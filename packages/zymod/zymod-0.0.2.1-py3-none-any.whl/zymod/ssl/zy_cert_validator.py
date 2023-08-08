import datetime
from typing import Any

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.x509 import Name, ObjectIdentifier, Certificate
from cryptography.x509.extensions import ExtensionNotFound
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding, ec, utils
from cryptography.hazmat.primitives import serialization, hashes
from happy_python import HappyLog

from zymod.event import ZyInternalEvent, ZyEventLevel
from zymod.ssl import ZyCert
from zymod.util import TimeDurationCalculator


class ZyCertValidator:
    """
    HTTP SSL证书校验器

    1、检查证书文件、密钥文件以及根证书文件有效性；
    2、确认证书文件和密钥文件是否匹配；
    3、导出证书信息
    """
    __cert: Certificate = None
    __cert_chain: Certificate = None
    __hlog = HappyLog.get_instance()
    __private_key: Any = None

    __cert_path: str = ''
    __root_cert_path: str = ''
    __private_key_path: str = ''
    __private_key_type: str = ''

    def __init__(self, cert_path: str, root_cert_path: str, private_key_path: str):
        self.__cert_path = cert_path
        self.__root_cert_path = root_cert_path
        self.__private_key_path = private_key_path

    @staticmethod
    def __get_nameoid_value(name: Name, oid: ObjectIdentifier) -> str:
        r = name.get_attributes_for_oid(oid)

        # <未包含在证书中>
        return r[0].value if r else "<未包含在证书中>"

    @staticmethod
    def __load_cert_path(file: str, desc: str) -> Certificate:
        try:
            with open(file, 'rb') as f_handler:
                return x509.load_pem_x509_certificate(data=f_handler.read(), backend=default_backend())
        except ValueError:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='无效的%s文件：%s' % (desc, file),
                                  trigger="无效的SSL证书文件")
        except OSError as e:  # IsADirectoryError | FileNotFoundError | ...
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='载入%s文件时，出现系统错误：%s' % (desc, e),
                                  trigger="无效的SSL证书文件")

    def __load_cert(self, file: str) -> None:
        self.__cert = self.__load_cert_path(file, 'SSL证书')

    def __load_root_cert(self, file: str) -> None:
        self.__cert_chain = self.__load_cert_path(file, 'SSL根证书')

    def __load_private_key(self) -> None:
        try:
            with open(self.__private_key_path, 'rb') as f_handler:
                self.__private_key = serialization.load_pem_private_key(data=f_handler.read(),
                                                                        password=None,
                                                                        backend=default_backend())
        except ValueError:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='无效的SSL密钥文件：%s' % self.__private_key_path,
                                  trigger='无效的SSL密钥文件')
        except OSError as e:  # IsADirectoryError | FileNotFoundError | ...
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='载入SSL密钥文件时，出现系统错误：%s' % e,
                                  trigger='载入SSL密钥文件时，出现系统错误')

    def __verify_rsa_signature(self, digest, cert_sign_hash_algo) -> None:
        signature_algorithm = utils.Prehashed(cert_sign_hash_algo)

        signature = self.__private_key.sign(data=digest,
                                            padding=padding.PSS(
                                                mgf=padding.MGF1(cert_sign_hash_algo),
                                                salt_length=padding.PSS.MAX_LENGTH),
                                            algorithm=signature_algorithm)

        self.__cert.public_key().verify(signature=signature,
                                        data=digest,
                                        padding=padding.PSS(
                                            mgf=padding.MGF1(cert_sign_hash_algo),
                                            salt_length=padding.PSS.MAX_LENGTH),
                                        algorithm=signature_algorithm)

    def __verify_ecdsa_signature(self, digest, cert_sign_hash_algo) -> None:
        signature_algorithm = ec.ECDSA(utils.Prehashed(cert_sign_hash_algo))

        signature = self.__private_key.sign(data=digest,
                                            signature_algorithm=signature_algorithm)
        self.__cert.public_key().verify(signature=signature,
                                        data=digest,
                                        signature_algorithm=signature_algorithm)

    def __step1_verify_cert_files(self) -> None:
        """
        验证证书（公钥）文件和根证书文件（如fullchain.pem, chain.pem）
        :return:
        """
        self.__load_cert(self.__cert_path)
        self.__load_root_cert(self.__root_cert_path)

    def __step2_verify_cert(self) -> None:
        """
        证书是否由指定CA机构颁发（如fullchain.pem->chain.pem）
        :return:
        """
        try:
            self.__cert_chain.public_key().verify(
                signature=self.__cert.signature,
                data=self.__cert.tbs_certificate_bytes,
                padding=padding.PKCS1v15(),
                algorithm=self.__cert.signature_hash_algorithm)
        except InvalidSignature:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='证书（%s）不是指定CA机构（%s）颁发的' % (self.__cert_path, self.__root_cert_path),
                                  trigger='证书不是由指定CA机构颁发')

    def __step3_verify_private_key_file(self) -> None:
        """
        验证密钥文件（如privkey.pem）
        :return:
        """
        self.__load_private_key()

    def __step4_verify_signature(self) -> None:
        """
        验证签名

        完整执行一次明文->密文（签名字符串）->明文的加解密流程，验证证书和密钥是否匹配（如fullchain.pem+privkey.pem）
        :return:
        """
        chosen_hash = self.__cert.signature_hash_algorithm
        hasher = hashes.Hash(chosen_hash)
        hasher.update(b'Hello world!')
        digest = hasher.finalize()

        try:
            # _EllipticCurvePrivateKey->ECDSA
            # _RSAPrivateKey->RSA
            private_key_type = type(self.__private_key).__name__

            if private_key_type == '_EllipticCurvePrivateKey':
                self.__private_key_type = 'ECDSA'
                self.__verify_ecdsa_signature(digest, chosen_hash)
            else:
                self.__private_key_type = 'RSA'
                self.__verify_rsa_signature(digest, chosen_hash)
        except InvalidSignature:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='签名验证失败，证书文件：%s，密钥文件：%s' % (self.__cert_path, self.__private_key_path),
                                  trigger='签名验证失败')

    def verify(self):
        self.__step1_verify_cert_files()
        self.__step2_verify_cert()
        self.__step3_verify_private_key_file()
        self.__step4_verify_signature()

    def dump_formatted_data(self) -> ZyCert:
        """
        导出格式化后的证书数据
        :return:
        """
        assert self.__cert

        dns_names: list[str] = list()
        common_name = self.__get_nameoid_value(self.__cert.subject, NameOID.COMMON_NAME)

        try:
            subject_alt_name_oid_value = \
                self.__cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value

            get_values_for_type_func = getattr(subject_alt_name_oid_value, 'get_values_for_type')

            for dns in get_values_for_type_func(x509.DNSName):
                dns_names.append(dns)
        except AttributeError:
            assert False
        except ExtensionNotFound:
            # ExtensionOID.SUBJECT_ALTERNATIVE_NAME属性不存在
            if len(dns_names) == 0:
                dns_names.append(common_name)

        time_duration = TimeDurationCalculator.calculate(self.__cert.not_valid_after, datetime.datetime.utcnow())

        output = ZyCert(domain=dns_names[0],
                        cert_path=self.__cert_path,
                        root_cert_path=self.__root_cert_path,
                        private_key_path=self.__private_key_path,
                        private_key_type=self.__private_key_type,
                        issued_to=ZyCert.IssuedTo(
                            common_name=common_name,
                            organization=self.__get_nameoid_value(self.__cert.subject, NameOID.ORGANIZATION_NAME),
                            organization_unit=self.__get_nameoid_value(self.__cert.subject,
                                                                       NameOID.ORGANIZATIONAL_UNIT_NAME)),
                        issued_by=ZyCert.IssuedBy(
                            common_name=self.__get_nameoid_value(self.__cert.issuer, NameOID.COMMON_NAME),
                            organization=self.__get_nameoid_value(self.__cert.issuer, NameOID.ORGANIZATION_NAME),
                            organization_unit=self.__get_nameoid_value(self.__cert.issuer,
                                                                       NameOID.ORGANIZATIONAL_UNIT_NAME)),
                        validity_period=ZyCert.ValidityPeriod(issued_on=self.__cert.not_valid_before,
                                                              expires_on=self.__cert.not_valid_after,
                                                              time_left=time_duration),
                        subject_alt_name=ZyCert.SubjectAltName(dns_names=dns_names))

        return output
