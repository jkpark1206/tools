#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import time
from datetime import datetime
from sqlalchemy import create_engine, desc, distinct, or_
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, BigInteger, LargeBinary, Float, SmallInteger
from sqlalchemy.dialects.postgresql import JSONB

# 注意：由于该模块跑在docker容器里，这里的数据库host，需要用到宿主机的ip
engine = create_engine(f'postgresql://postgres:123456@192.168.1.186:25432/ys_yishi')
# engine = create_engine(f'postgresql://postgres:123456@192.168.5.223:25432/ys_yishi')
Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()

import base64


class Base64Crypto:

    def crypoto(self, data):
        if not data:
            data = ""
        return base64.b64encode(str.encode(data))

    def decode(self, decode_data):
        try:
            return base64.b64decode(decode_data.decode()).decode()
        except Exception as e:
            # logger.log('ERROR', f'解码失败原因{e}')
            return ''


av_dict = {
    'N': '- 网络（N），漏洞可被远程利用，攻击者可通过网络（包括internet）远程发起攻击。',
    'A': '- 相邻网络攻击（A），攻击仅限于在逻辑相邻的网络拓扑。攻击必须从同一各共享物理网络（例如，蓝牙或 IEEE 802.11）或逻辑网络（例如，本地 IP 子网）发起，或者从安全或其他受限的管理域（如MPLS、安全 VPN 到管理网络区域）发起。',
    'L': """- 本地（L），
  - 攻击者通过本地（如键盘、控制台）或者远程（如SSH）访问目标系统。
  - 攻击者利用他人执行操作（如，诱使合法用户打开恶意文档）。""",
    'P': '- 物理（P），攻击者必须物理接触或操纵该组件。',
}

#  攻击复杂度（AC）
ac_dict = {
    'L': '- 低（L）攻击难度低，不需要特殊设备或环境，对攻击者本身能力要求低。',
    'H': """- 高（H）攻击难度高，需要具备以下条件之一才可攻击成功：
  - 必须收集攻击目标的环境信息。（如，配置信息、序列号或共享机密信息。）
  - 必须准备目标环境以提高利用漏洞的可靠性。（如，重复利用此漏洞赢得争用条件，或克服高级漏洞利用缓解技术）
  - 攻击者必须将自己诸如目标和受害者请求的资源之间的逻辑网络路径中，以便读取和/或修改网络通信（如：中间人攻击。）""",
}

#  权限要求（PR）
pr_dict = {
    'N': '- 无要求（N），攻击者不需要访问目标系统。',
    'L': '- 低权限要求（L），攻击者需要普通用户功能的权限。',
    'H': '- 高权限要求（H），攻击者需要管理控制权限。',
}

#  用户交互（UI）
ui_dict = {
    'N': '- 无交互（N），攻击者不需要其他用户的操作。',
    'R': '- 有交互（R），攻击者需要其他用户进行一些操作。如，只有在系统管理员安装应用期间才能进行攻击。',
}

#  影响范围（S）
s_dict = {
    'C': '- 会扩散（C），漏洞影响范围会扩大到其他组件，受攻击的组件和受影响的组件不是同一个，并且由不同的安全机构（如，应用程序、操作系统、固件、沙盒环境）管理。',
    'U': '- 不扩散（U），漏洞影响范围不会扩大到其他组件，或者受攻击的组件和受影响的组件在同一个安全机构（如，应用程序、操作系统、固件、沙盒环境）管理。',
}

#  机密性影响度（C）
c_dict = {
    'H': '- 高（H），完全失去机密性，导致受影响组件中的所有资源都泄露给攻击者。或者，仅获取某些受限信息，但披露的信息会产生直接、严重的影响。例如，攻击者窃取管理员的密码或 Web 服务器的私有加密密钥。',
    'L': '- 低（L），部分机密性损失。攻击者获得对某些受限制信息的访问权限，但无法控制获得的信息，或者损失的数量或种类受限。信息泄露不会对受影响的组件造成直接的严重损失。',
    'N': '- 无（N），无机密性损失。',
}

#  完整性影响度（I）
i_dict = {
    'H': '- 高（H），完全丧失了完整性，或者完全失去了保护。例如，攻击者能够修改受影响组件保护的所有文件。或者，只能修改某些文件，但恶意修改会对受影响的组件造成直接、严重的后果。',
    'L': '- 低（L），攻击者能够修改数据，但无法控制修改的后果，或者修改的数量是有限的。数据修改不会对受影响的组件产生直接、严重的影响。',
    'N': '- 无（N），受影响组件不会失去完整性。',
}

#  可用性影响度（A）
a_dict = {
    'H': '- 高（H），完全失去可用性，攻击者可以完全拒绝对受影响组件中的资源的访问。或者，攻击者能够拒绝某些可用性，但可用性的丢失会给受影响的组件带来直接而严重的后果（如，攻击者无法中断现有连接，但可以阻止新连接；攻击者可以反复利用漏洞，每次攻击造成内存泄露，重复攻击后导致服务不可用）。',
    'L': '- 低（L），性能降低或资源可用性中断。攻击者无法实现受影响组件完全拒绝向合法用户提供服务。受影响组件中的资源要么始终部分可用，要么仅在部分时间完全可用，但总体而言，受影响的组件不会产生直接的严重后果。',
    'N': '- 无（N），对受影响组件中的可用性没有影响。',
}

##cvss2的基准
#  攻击途径(AV)


av_dict_2 = {
    'N': '- 网络（N），只能通过本地访问来利用的漏洞，要求攻击者拥有对易受攻击的系统或本地（shell）帐户的物理访问。 局部例子，可利用的漏洞是外围攻击，例如 Firewire/USB DMA 攻击，以及本地权限提升（例如，sudo）。',
    'A': '- 相邻网络攻击（A），可通过相邻网络访问利用的漏洞要求攻击者能够访问易受攻击软件的广播域或冲突域。 本地网络的示例包括本地 IP 子网、蓝牙、IEEE 802.11 和本地以太网段。',
    'L': '- 本地（L），可通过网络访问利用的漏洞意味着易受攻击的软件绑定到网络堆栈，攻击者不需要本地网络访问或本地访问。 这种漏洞通常被称为“可远程利用”。 网络攻击的一个例子是 RPC 缓冲区溢出。',
}

#  攻击复杂度（AC）
ac_dict_2 = {
    'L': """- 低（L）攻击难度低，不存在专门的准入条件或情有可原的情况，以下是示例：
  - 受影响的产品通常需要访问广泛的系统和用户，可能是匿名和不受信任的（例如，面向 Internet 的 Web 或邮件服务器）。
  - 受影响的配置是默认的或普遍存在的。
  - 攻击可以手动执行，只需要很少的技能或额外的信息收集。
  - “比赛条件”是一种懒惰的条件（即，它在技术上是一场比赛，但很容易获胜）。""",
    'M': """- 中（M）攻击难度中，访问条件有些特殊，以下是示例：
  - 攻击方仅限于具有某种授权级别的一组系统或用户，可能不受信任。 在成功发起攻击之前，必须收集一些信息。
  - 受影响的配置是非默认的，并且通常不配置（例如，当服务器通过特定方案执行用户帐户身份验证时存在漏洞，但对于其他身份验证方案不存在）。
  - 该攻击需要少量社交工程，有时可能会欺骗谨慎的用户（例如，修改网络浏览器状态栏以显示虚假链接的网络钓鱼攻击，在发送 IM 漏洞之前必须在某人的“好友”列表中）。""",
    'H': """- 高（H）攻击难度高，需要具备以下条件之一才可攻击成功：
  - 例如，在大多数配置中，攻击方必须已经拥有提升的权限或欺骗攻击系统之外的其他系统（例如，DNS 劫持）。攻击依赖于社会工程方法，知识渊博的人很容易发现。
  - 例如，受害者必须执行几个可疑或非典型行为。易受攻击的配置在实践中很少见。如果存在竞争条件，则窗口非常窄。""",
}

#  身份验证（Au）
au_dict_2 = {
    'M': '- 多种（M）利用该漏洞需要攻击者进行两次或多次身份验证，即使每次都使用相同的凭据。 例如，攻击者除了提供凭据以访问托管在该系统上的应用程序外，还对操作系统进行身份验证。',
    'S': '- 单个（S）访问和利用该漏洞需要一个身份验证实例。',
    'N': '- 无（N）访问和利用漏洞不需要身份验证。',
}

#  机密性影响度（C）
c_dict_2 = {
    'C': '- 完整（C）存在全面信息泄露，导致所有系统文件被泄露。 攻击者能够读取系统的所有数据（内存、文件等）。',
    'P': '- 部分（P）有大量信息披露。 可以访问某些系统文件，但攻击者无法控制获取的内容，或者丢失的范围受到限制。 一个示例是仅泄露数据库中某些表的漏洞。',
    'N': '- 无（N）对系统的机密性没有影响。',
}

#  完整性影响度（I）
i_dict_2 = {
    'C': '- 完整（C）系统完整性完全妥协。 系统保护完全丧失，导致整个系统受到损害。 攻击者能够修改目标系统上的任何文件。',
    'P': '- 部分（P）可以修改某些系统文件或信息，但攻击者无法控制可以修改的内容，或者攻击者可以影响的范围有限。 例如，系统或应用程序文件可能被覆盖或修改，但攻击者无法控制哪些文件受到影响，或者攻击者只能在有限的上下文或范围内修改文件。',
    'N': '- 无（N）对系统的完整性没有影响。',
}

#  可用性影响度（A）
a_dict_2 = {
    'C': '- 完整（C）受影响的资源完全关闭。 攻击者可以使资源完全不可用。',
    'P': '- 部分（P）资源可用性降低或中断。 一个例子是基于网络的洪水攻击，它允许有限数量的成功连接到 Internet 服务。',
    'N': '- 无（N）对系统的可用性没有影响。',
}
aes_crypto = Base64Crypto()


class CVECNInfo(Base):
    __tablename__ = 'ys_cve_cn_info'
    id = Column(Integer, primary_key=True)  # 主键
    name = Column(LargeBinary)  # cve的中文名称
    cve_id = Column(String(30))  # cve的id
    cnnvd_id = Column(String(100), default='')  # CNNVD的编号
    cnnvd_url = Column(String(100), default='')  # CNNVD的url地址
    severity = Column(Integer, default=0)  # 危害等级: 0-未知，1-低，2-中，3-高，4-超危
    desc = Column(LargeBinary)  # cve漏洞简介
    solution = Column(LargeBinary)  # cve漏洞公告或修复建议
    related_cwe = Column(String(30), default='')  # cve关联的cwe
    cvss_3 = Column(Float)  # cvss_3评分
    cvss_2 = Column(Float)  # cvss_2评分
    cve_av_3 = Column(LargeBinary)  # 攻击途径
    cve_ac_3 = Column(LargeBinary)  # 攻击复杂度
    cve_pr = Column(LargeBinary)  # 权限要求（PR）
    cve_ui = Column(LargeBinary)  # 用户交互（UI）
    cve_s = Column(LargeBinary)  # 影响范围（S）
    cve_c_3 = Column(LargeBinary)  # 机密性影响度（C）
    cve_i_3 = Column(LargeBinary)  # 完整性影响度（I）
    cve_a_3 = Column(LargeBinary)  # 可用性影响度（A）
    cve_au = Column(LargeBinary)  # 身份验证（Au）

    cve_av_2 = Column(LargeBinary)  # 攻击途径
    cve_ac_2 = Column(LargeBinary)  # 攻击复杂度
    cve_c_2 = Column(LargeBinary)  # 机密性影响度（C）
    cve_i_2 = Column(LargeBinary)  # 完整性影响度（I）
    cve_a_2 = Column(LargeBinary)  # 可用性影响度（A）

    published = Column(String(30))  # 发布时间
    last_modified = Column(String(30))  # 更新时间

    # source = Column(String(200))  # 漏洞来源
    # vuln_type = Column(String(100))  # 漏洞类型
    # thrtype = Column(String(30))  # 威胁类型：远程、本地等等
    # company = Column(String(100))  # 厂商
    # refs = Column(Text)  # 更新参考网址
    # software_list = Column(Text)  # 受影响实体

    def cve_display(self, cve_info, cve3_dict, cve2_dict=None):
        if not cve_info:
            return None
        val = aes_crypto.decode(cve_info).strip()
        for k, v in cve3_dict.items():
            if v == val:
                return k
        if cve2_dict:
            for k, v in cve2_dict.items():
                if v == val:
                    return k
        return None

    @property
    def dict(self):

        if self.published:
            a_list = self.published.split('T')[0].split('-')
            published = f'{a_list[0]}年{a_list[1]}月{a_list[2]}日'
        else:
            published = ''
        if self.cvss_3:
            self.cve_av = self.cve_av_3
            self.cve_ac = self.cve_ac_3
            self.cve_c = self.cve_c_3
            self.cve_i = self.cve_i_3
            self.cve_a = self.cve_a_3
        else:
            self.cve_av = self.cve_av_2
            self.cve_ac = self.cve_ac_2
            self.cve_c = self.cve_c_2
            self.cve_i = self.cve_i_2
            self.cve_a = self.cve_a_2
        return {
            'id': self.id,
            'name': aes_crypto.decode(self.name) if self.name else None,
            'cve_id': self.cve_id,
            'cnnvd_id': self.cnnvd_id,
            'cnnvd_url': self.cnnvd_url,
            'severity': self.severity,
            'desc': aes_crypto.decode(self.desc) if self.desc else None,
            'solution': aes_crypto.decode(self.solution) if self.solution else None,
            'cvss_3': self.cvss_3 if self.cvss_3 else None,
            'cvss_2': self.cvss_2 if self.cvss_2 else None,
            'cve_av': self.cve_display(self.cve_av, av_dict, av_dict_2),
            'cve_ac': self.cve_display(self.cve_ac, ac_dict, ac_dict_2),
            'cve_pr': self.cve_display(self.cve_pr, pr_dict),
            'cve_ui': self.cve_display(self.cve_ui, ui_dict),
            'cve_s': self.cve_display(self.cve_s, s_dict),
            'cve_c': self.cve_display(self.cve_c, c_dict, c_dict_2),
            'cve_i': self.cve_display(self.cve_i, i_dict, i_dict_2),
            'cve_a': self.cve_display(self.cve_a, a_dict, a_dict_2),
            'cve_au': self.cve_display(self.cve_au, au_dict_2),
            'related_cwe': self.related_cwe,
            'published': published,
        }

    @property
    def down_dict(self):
        # from anafirm.cve_cve_info import av_dict, a_dict, ac_dict, pr_dict, ui_dict, s_dict, c_dict, i_dict, \
        #     au_dict_2, av_dict_2, ac_dict_2, a_dict_2, i_dict_2, c_dict_2
        if self.published:
            a_list = self.published.split('T')[0].split('-')
            published = f'{a_list[0]}年{a_list[1]}月{a_list[2]}日'
        else:
            published = ''

        return {
            'id': self.id,
            'name': aes_crypto.decode(self.name) if self.name else None,
            'cve_id': self.cve_id,
            'cnnvd_id': self.cnnvd_id,
            'cnnvd_url': self.cnnvd_url,
            'severity': self.severity,
            'desc': aes_crypto.decode(self.desc) if self.desc else None,
            'solution': aes_crypto.decode(self.solution) if self.solution else None,
            'cvss_3': self.cvss_3 if self.cvss_3 else None,
            'cvss_2': self.cvss_2 if self.cvss_2 else None,
            'cve_pr': self.cve_display(self.cve_pr, pr_dict),
            'cve_ui': self.cve_display(self.cve_ui, ui_dict),
            'cve_s': self.cve_display(self.cve_s, s_dict),
            'cve_au': self.cve_display(self.cve_au, au_dict_2),
            'related_cwe': self.related_cwe,
            'published': published,

            'cve_av_3': self.cve_display(self.cve_av_3, av_dict),
            'cve_ac_3': self.cve_display(self.cve_ac_3, ac_dict),
            'cve_c_3': self.cve_display(self.cve_c_3, c_dict),
            'cve_i_3': self.cve_display(self.cve_i_3, i_dict),
            'cve_a_3': self.cve_display(self.cve_a_3, a_dict),

            'cve_av_2': self.cve_display(self.cve_av_2, av_dict, av_dict_2),
            'cve_ac_2': self.cve_display(self.cve_ac_2, ac_dict, ac_dict_2),
            'cve_c_2': self.cve_display(self.cve_c_2, c_dict, c_dict_2),
            'cve_i_2': self.cve_display(self.cve_i_2, i_dict, i_dict_2),
            'cve_a_2': self.cve_display(self.cve_a_2, a_dict, a_dict_2),
        }


class SoftWareLicense(Base):
    """开源软件对应的开源许可证表"""
    __tablename__ = 'ys_license_info'
    id = Column(Integer, primary_key=True)  # 主键
    soft_name = Column(String(100), index=True)  # 开源软件的名称
    soft_version = Column(Text)  # 开源软件的版本号列表: 默认空表示所有的版本
    license_name = Column(LargeBinary)  # 开源软件的许可证名称列表

    @property
    def dict(self):
        return {
            'id': self.id,
            'soft_name': self.soft_name,
            'soft_version': json.loads(self.soft_version),
            'license_name': json.loads(aes_crypto.decode(self.license_name)),
        }


class ScanResult(Base):
    '''FirmWare扫描结果表'''
    __tablename__ = 'ys_firmware_scan_result'
    id = Column(Integer, primary_key=True)  # 主键
    # task_id = Column(Integer, ForeignKey("ys_firmware_scan_task.id"), index=True,
    #                  comment="FirmWare扫描任务id")  # FirmWare扫描任务id
    is_delete = Column(Boolean, default=False, comment="是否删除")
    meta = Column(Text, comment="固件任务的元数据")  # 固件任务的元数据
    plugin = Column(JSONB, comment='插件分析结果', default={})

    cwe_file = Column(Text, default=json.dumps({}), comment="")
    # 固件漏洞文件对应的漏洞信息{'file_name1': {'file_path': None, 'cwe_name': ['cwe123', 'cwe456']},}
    cwe_count = Column(Text, default=json.dumps({}), comment="cwe扫描结果数量统计")  # cwe扫描结果数量统计
    cve_count = Column(Text, default=json.dumps({}), comment="cve扫描结果数量统计")  # cve扫描结果数量统计

    # task = relationship("FirmWareScanTask", backref="task_result")
    task_id = Column(Integer, index=True)  # FirmWare扫描任务id
    create_time = Column(DateTime, default=datetime.now)  # 创建时间

    @property
    def dict(self):
        count_data = {'all': 0, 'unknown': 0, 'lower': 0, 'middle': 0, 'high': 0, 'super': 0}
        cve_count_data = json.loads(self.cve_count)
        cwe_count_data = json.loads(self.cwe_count)
        self_plugin = json.loads(self.plugin)
        if "cve_lookup" in self_plugin:
            if not cve_count_data:
                cve_count_data = count_data
        if "cwe_checker" in self_plugin:
            if not cwe_count_data:
                cwe_count_data = count_data

        print('INFOR', f'cwe_count_data:{cwe_count_data}')
        ans = {
            "id": self.id,
            "task_id": self.task_id,
            "meta": json.loads(self.meta) if self.meta else {},
            "cwe_file": json.loads(self.cwe_file) if self.cwe_file else {},
            # "cwe_count": json.loads(self.cwe_count) if self.cwe_count else {},
            "cwe_count": cwe_count_data,
            # "cve_count": json.loads(self.cve_count) if self.cve_count else {},
            "cve_count": cve_count_data,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for plugin_name in REPORT_PLUGIN.values():
            ans.update({plugin_name: json.loads(self.plugin).get(plugin_name, {})})
        for plugin_name in [ys_cpu, ys_type]:
            ans.update({plugin_name: json.loads(self.plugin).get(plugin_name, {})})
        return ans


def cvss3_rank(score: float):
    """
    根据cvss3评分判断漏洞等级
    :param score:
    :return:
    """
    if score == 0:
        return 0  # 未知
    elif 0.1 <= score <= 3.9:
        return 1  # 低
    elif 4.0 <= score <= 6.9:
        return 2  # 中
    elif 7.0 <= score <= 8.9:
        return 3  # 高
    else:
        return 4  # 超


def cvss2_rank(score: float):
    """
    根据cvss2评分判断漏洞等级
    :param score:
    :return:
    """
    if 0 <= score <= 3.9:
        return 1  # 低
    elif 4.0 <= score <= 6.9:
        return 2  # 中
    else:
        return 3  # 高


class CWEInfo(Base):
    __tablename__ = 'ys_cwe_info'
    id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(50), index=True)  # cwe的编号
    cn_name = Column(LargeBinary)  # cwe的中文名称
    desc = Column(LargeBinary)  # cwe描述
    cvss = Column(Float, nullable=True)  # 平均cvss评分
    available = Column(Integer)  # 可利用性
    result_list = Column(Text)  # 常见后果列表
    re_sug = Column(LargeBinary)  # 修复建议
    severity = Column(Integer)  # cve的严重程度
    published = Column(String(30))  # 发布时间
    cve_list = Column(JSONB, comment="关联的cve列表")

    @property
    def dict(self):
        return {
            "name": self.name,
            "cn_name": aes_crypto.decode(self.cn_name),
            "desc": aes_crypto.decode(self.desc),
            "cvss": self.cvss if self.cvss else None,
            "available": self.available,
            "result_list": json.loads(self.result_list),
            "re_sug": aes_crypto.decode(self.re_sug),
            "severity": self.severity,
        }


class LicenseInfo(Base):
    """开源许可证表"""
    __tablename__ = 'ys_license_detail'
    id = Column(Integer, primary_key=True)  # 主键
    lic_name = Column(LargeBinary)  # 许可证名称
    lic_type = Column(String(50))  # 类型
    lic_intro = Column(LargeBinary)  # 简介
    lic_web = Column(LargeBinary)  # 官网
    content = Column(LargeBinary)  # 内容
    lic_perm = Column(LargeBinary)  # 许可权限
    pro_perm = Column(LargeBinary)  # 禁止权限
    lic_con = Column(LargeBinary)  # 许可证条件
    update_time = Column(DateTime, default=datetime.now)  # 更新时间

    @property
    def dict(self):
        return {
            'id': self.id,
            'lic_name': aes_crypto.decode(self.lic_name),
            'lic_type': self.lic_type,
            'lic_intro': aes_crypto.decode(self.lic_intro).replace("\\r\\n", "\r\n"),
            'lic_web': aes_crypto.decode(self.lic_web),
            'content': aes_crypto.decode(self.content).replace("\\r\\n", "\r\n"),
            'lic_perm': aes_crypto.decode(self.lic_perm),
            'pro_perm': aes_crypto.decode(self.pro_perm),
            'lic_con': aes_crypto.decode(self.lic_con),
            'update_time': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class TaskHomology(Base):
    __tablename__ = 'ys_task_homology'
    id = Column(Integer, primary_key=True)  # 主键
    # task_id = Column(Integer, ForeignKey("ys_firmware_scan_task.id", ondelete="SET NULL"), nullable=True,
    #                     comment="同源性分析结果关联任务id", index=True)
    # task = relationship("FirmWareScanTask", backref="task_homology")
    file_path = Column(String(200), comment="组件文件路径")
    func_data = Column(JSONB, comment="函数分析结果数据")


class TaskQueue(Base):
    '''扫描任务队列表'''
    __tablename__ = 'ys_task_queue'
    id = Column(Integer, primary_key=True)  # 主键
    task_type = Column(Integer, nullable=False)  # 任务类型：0-扫描任务，1-对比任务
    task_status = Column(Integer, nullable=False)  # 扫描任务状态
    update_plugin_list = Column(JSONB, comment="新版较旧版多出的插件，例如cwe、homology插件")


class CVEFile(Base):
    '''CVE扫描结果文件信息存储表'''
    __tablename__ = 'ys_cve_file'
    id = Column(Integer, primary_key=True)  # 主键
    is_delete = Column(Boolean, default=False)
    name = Column(Text, comment="cve漏洞文件名")  # cve漏洞文件名
    path = Column(Text, comment="cve漏洞文件路径")  # cve漏洞文件路径
    vuln = Column(Text, comment="漏洞信息表")  # 漏洞信息表：共2个，高危1个，中危1个 {'all': 2, 'high':1, 'middle': 1}
    cve_data = Column(Text, comment="漏洞详情统计表")  # 漏洞详情统计表：
    software = Column(Text, comment="软件列表")  # 软件列表
    soft_data = Column(JSONB, default={}, comment="文件组件统计信息")
    solution = Column(Text, default='', comment="修复建议")  # 修复建议

    task_id = Column(Integer)  # FirmWare扫描任务id
    # task = relationship("FirmWareScanTask", backref="cve_file_data")


class CWEFile(Base):
    '''CWE扫描结果文件信息存储表'''
    __tablename__ = 'ys_cwe_file'
    id = Column(Integer, primary_key=True)  # 主键
    is_delete = Column(Boolean, default=False)
    name = Column(Text, comment="cwe漏洞文件名")  # cwe漏洞文件名
    path = Column(Text, comment="cwe漏洞文件路径")  # cwe漏洞文件路径
    vuln = Column(Text, comment="漏洞信息表")  # 漏洞信息表：共2个，高危1个，中危1个 {'all': 2, 'high':1, 'middle': 1}
    cwe_data = Column(Text, comment="漏洞详情统计表")  # 漏洞详情统计表：

    task_id = Column(Integer, index=True)  # FirmWare扫描任务id
    # task_id = Column(Integer, ForeignKey("ys_firmware_scan_task.id", ondelete="SET NULL"), index=True)  # FirmWare扫描任务id
    # task = relationship("FirmWareScanTask", backref="cwe_file_data")


class LicenseBaseInfo(Base):
    """许可证详细信息"""
    __tablename__ = "ys_license_base_info"
    id = Column(Integer, primary_key=True)
    lj_license_key = Column(String(255), comment="许可证名称")
    title = Column(Text, comment="许可证全称")
    license_risk_level = Column(Text, comment="风险等级")
    category_en = Column(String(255), comment="类型_英文")
    category_ch = Column(String(255), comment="类型_中文")
    osi_approval = Column(SmallInteger, comment="OSI收录 1收录 0未收录")
    fsf_approval = Column(SmallInteger, comment="FSF收录 1收录 0未收录")
    spdx_approval = Column(SmallInteger, comment="FSF收录 1收录 0未收录")
    spdx_id = Column(String(255), comment="SPDX Id")
    spdx_url = Column(Text, comment="SPDX链接")
    publication_year = Column(String(255), comment="发布日期")
    text_urls = Column(Text, comment="原文链接")
    full_text = Column(Text, comment="全文")
    quick_summary_en = Column(Text, comment="摘要-英文")
    quick_summary_ch = Column(Text, comment="摘要-中文")
    keywords = Column(Text, comment="关键词")
    owner_name = Column(Text, comment="所有者名称")
    owner_type = Column(String(50), comment="所有者类型")
    owner_alias = Column(String(255), comment="所有者别名")
    owner_home_page = Column(Text, comment="所有者主页")
    owner_contact_information = Column(String(255), comment="所有者联系信息")
    owner_notes = Column(Text, comment="所有者说明")
    n_used = Column(Integer, comment="使用频率")
    is_add = Column(Integer, comment="是否新增")
    update_time = Column(DateTime, comment="更新时间")
    lawer_verified = Column(SmallInteger, comment="已通过律师验证")
    map_id = Column(Integer, comment="")
    rank = Column(Integer, comment="")
    license_text = Column(String(255), comment="原文下载链接")
    create_time = Column(DateTime, comment="创建时间")
    source = Column(String(16), comment="来源")


class LicenseToDo(Base):
    """许可证相关条款"""
    __tablename__ = "ys_license_to_do"
    id = Column(Integer, primary_key=True)
    lj_license_key = Column(String(255), comment="许可证名称-短")
    slug_name = Column(String(255), comment="许可证名称-长")
    belong = Column(String(255), comment="条款类型-英文， can-许可权限， must-许可证条件 mustnot、cannot-禁止权限")
    title = Column(String(255), comment="条款标题-英文")
    title_ch = Column(String(255), comment="条款标题-中文")
    title_desc = Column(String(255), comment="条款类型描述")
    description = Column(Text, comment="条款描述-英文")
    description_ch = Column(Text, comment="条款描述-中文")
    dimensions_explain = Column(Text, comment="条款解释")
    map_id = Column(Integer, comment="")
    create_time = Column(DateTime, comment="创建时间")
    update_time = Column(DateTime, comment="创建时间")


class CVERelTask(Base):
    """
    CVE关联任务表
    """
    __tablename__ = "ys_cve_rel_task"
    id = Column(Integer, primary_key=True)
    cve_id = Column(String(20), nullable=False, comment="CVE 编号", index=True)
    cnnvd_id = Column(String(20), comment="CNNVD 编号", index=True)
    task_id = Column(Integer, nullable=False, comment="关联任务id", index=True)
    is_delete = Column(Boolean, default=False, comment="是否删除")


class CWERelTask(Base):
    """
    CWE关联任务表
    """
    __tablename__ = "ys_cwe_rel_task"
    id = Column(Integer, primary_key=True)
    cwe_id = Column(String(10), nullable=False, comment="CWE 编号", index=True)
    task_id = Column(Integer, nullable=False, comment="关联任务id", index=True)
    is_delete = Column(Boolean, default=False, comment="是否删除")


class LicenseRelTask(Base):
    """
    CWE关联任务表
    """
    __tablename__ = "ys_license_rel_task"
    id = Column(Integer, primary_key=True)
    is_delete = Column(Boolean, nullable=False, default=False)
    license_name = Column(String(100), nullable=False, comment="许可证缩写", index=True)
    task_id = Column(Integer, nullable=False, comment="关联任务id", index=True)


class FirmWareScanTask(Base):
    '''FirmWare扫描任务表'''
    __tablename__ = 'ys_firmware_scan_task'
    # uuid = Column(String(100), index=True, comment="任务uuid")  # 任务uuid
    # task_name = Column(String(100), nullable=False, index=True, comment="任务名")  # 任务名
    # file_name = Column(String(100), default='', comment="文件名")  # 文件名
    # file_md5 = Column(String(100), default='', index=True, comment="文件md5值")  # 文件md5值
    # device_name = Column(String(100), default='', comment="设备名称")  # 设备名称
    # device_part = Column(String(100), default='', comment="设备类型")  # 设备类型
    # device_class = Column(String(100), default='', comment="设备")  #
    # version = Column(String(100), default='', comment="设备版本")  # 设备版本
    # vendor = Column(String(100), default='', comment="设备厂商")  # 设备厂商
    # plugin = Column(Text, comment="插件列表")  # 插件列表{'plugin': ['file_type', 'binwalk']}
    #
    # firmware_path = Column(Text, default='', comment="文件存储路径")  # 文件存储路径
    # vulnerable_file_path = Column(Text, default=json.dumps([]), comment="文件名")  # 固件漏洞文件存储路径['/mnt/yishi/test']
    # start_time = Column(DateTime, comment="开始时间")  # 开始时间
    # end_time = Column(DateTime, comment="结束时间")  # 结束时间
    # process = Column(Float, default=0.0, comment="任务进度")  # 任务进度
    # process_str = Column(String(50), default='0/0', comment="任务进度数量对比")  # 任务进度
    #
    # task_lib_tag = Column(Boolean, default=False, comment="是否关联固件库 True-关联 False-不关联")
    # task_run_tag = Column(Boolean, default=False, comment="是否存在关联固件库并且已完成 True-存在 False-存在")
    # copy_uuid = Column(String(100), default='', comment="被覆盖关联任务的uuid 前提是旧任务已完成")
    # # 若存在旧的关联库任务并且已完成, 重新扫描时可以复用之前扫描的结果
    # risk_db_version = Column(String(10), default='', comment="漏洞库版本")  # 漏洞库版本
    # system_version = Column(String(30), default='', comment="系统版本")  # 系统版本
    #
    # strategy_str = Column(String(150), default='', index=True, comment="策略字段")
    # strategy_id = Column(Integer, index=True, comment="策略id, -1 表示原始策略已删除")
    id = Column(Integer, primary_key=True)
    is_delete = Column(Boolean, default=False, comment="是否删除")
    plugin = Column(Text, comment="插件列表")  # 插件列表{'plugin': ['file_type', 'binwalk']}
    strategy_str = Column(String(350), default='', comment="")
    plugin_child_dict = Column(Text, comment="子插件列表")


class TaskWhite(Base):
    __tablename__ = "ys_task_white"
    id = Column(Integer, primary_key=True)
    is_delete = Column(Boolean, default=False, comment="是否删除")
    # task_id = Column(
    #     Integer,
    #     ForeignKey("ys_firmware_scan_task.id", ondelete="SET NULL"),
    #     nullable=True,
    #     comment="关联任务id",
    #     index=True,
    # )
    # task = relationship("FirmWareScanTask", backref="task_white")
    software_white = Column(JSONB, default={}, comment="任务软件成分白名单信息")
    cve_white = Column(JSONB, default={}, comment="任务CVE白名单信息")
    cve_count = Column(JSONB, default={}, comment="任务CVE总删减数据")
    last_update_user = Column(String(50), comment="最后一次更新者")


class Strategy(Base):
    __tablename__ = "ys_task_strategy"
    id = Column(Integer, primary_key=True)
    is_delete = Column(Boolean, default=False, comment="是否删除")
    name = Column(String(100), nullable=False, index=True, comment="策略名称")
    plugin_list = Column(JSONB, nullable=False, comment="插件列表")
    plugin_child_dict = Column(JSONB, default={}, comment="子插件列表")
    plugin_str = Column(String(20), nullable=False, comment="插件列表字符串")
    strategy_str = Column(String(150), default='', comment="策略字段")
    lib_tag = Column(Boolean, default=False, comment="是否关联固件库 True-关联 False-不关联")
    cvss_info = Column(JSONB, comment="自定义cvss")
    cvss_2 = Column(Boolean, default=False, comment="是否有自定义cvss2 True-有 False-没有")
    cvss_3 = Column(Boolean, default=False, comment="是否有自定义cvss3 True-有 False-没有")
    origin_default = Column(Boolean, default=False, comment="是否是初始默认项 True-是 False-不是")
    create_username = Column(String(100), comment="创建人名称")

    cvss_id = Column(
        Integer,
        ForeignKey("ys_task_strategy_cvss.id", ondelete="SET NULL"),
        nullable=True,
        comment="关联CVSS的id",
        index=True,
    )
    cvss = relationship("StrategyCVSS", backref="strategy_cvss")
    cvss_name = Column(String(100), comment="CVSS规则名称")


class StrategyCVSS(Base):
    __tablename__ = "ys_task_strategy_cvss"
    id = Column(Integer, primary_key=True)
    is_delete = Column(Boolean, default=False, comment="是否删除")
    name = Column(String(100), nullable=False, index=True, comment="白名单规则名称")
    cvss_info = Column(JSONB, nullable=False, comment="自定义cvss")
    create_username = Column(String(100), nullable=False, comment="创建人名称")
    create_time = Column(DateTime, default=datetime.now)  # 创建时间
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间


class User(Base):
    '''用户表User'''
    __tablename__ = 'ys_users'
    id = Column(Integer, primary_key=True)  # 主键
    username = Column(String(100), index=True)  # 用户名
    password = Column(String(200), nullable=False)  # 密码hash
    permissions = Column(Text, nullable=True)  # 权限字段
    is_external = Column(Boolean, default=False)  # 是否是来自外部的用户（如用户管理平台）
    color = Column(String(30), default="", comment="主题色")
    strategy_id = Column(
        Integer
    )


class ProductVersion(Base):
    """组件版本号"""
    __tablename__ = "ys_nvd_versions"
    id = Column(Integer, primary_key=True)
    vendor = Column(String(255), comment="供应商")
    product = Column(String(255), index=True, comment="产品")
    version = Column(String(255), comment="版本号")
    create_time = Column(DateTime, comment="创建时间")
    update_time = Column(DateTime, comment="更新时间")
    license_list = Column(JSONB, comment="许可证列表")


class SBOMDependency(Base):
    """
    物料清单-间接依赖关系表
    """
    __tablename__ = "ys_sbom_dependency"
    id = Column(Integer, primary_key=True)
    component = Column(String(50), nullable=False, comment="组件名称", index=True)
    version = Column(String(50), default='', comment="组件版本")
    dependency_name = Column(LargeBinary, comment="依赖名称")
    dependency_version = Column(LargeBinary, comment="依赖版本")
    source = Column(LargeBinary, comment="来源")

    @property
    def dict(self):
        return {
            "component": self.component,
            "version": self.version,
            "dependency_name": aes_crypto.decode(self.dependency_name),
            "dependency_version": aes_crypto.decode(self.dependency_version),
            "source": aes_crypto.decode(self.source)
        }


class SoftVersionRelTask(Base):
    """
    软件成分关联任务表
    """
    __tablename__ = "ys_soft_version_rel_task"
    id = Column(Integer, primary_key=True)
    is_delete = Column(Boolean, default=False)
    soft_name = Column(String(100), nullable=False, comment="软件名称", index=True)
    soft_version = Column(String(100), nullable=False, comment="软件版本", index=True)
    # soft_str = soft_name:soft_version
    soft_str = Column(String(200), nullable=False, comment="软件名称", index=True)
    task_id = Column(Integer, nullable=False, comment="关联任务id", index=True)




def check_sbom(product, version):
    query_list = session.query(SBOMDependency).filter(SBOMDependency.component == product,
                 SBOMDependency.version ==  version).all()
    for query in query_list:
        print(query.dict)




check_sbom(
    "openssl",
    "1.1.1"
)









