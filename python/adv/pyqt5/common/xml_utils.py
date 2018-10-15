# coding:utf-8
import os
from contextlib import contextmanager
from xml.dom import minidom

from xml.etree.ElementTree import ElementTree, Element

from common.const import CONST
from common.logger import log


def init(filename):
    xml = minidom.Document()
    root = xml.createElement('root')
    xml.appendChild(root)

    text_node = xml.createElement('project')
    root.appendChild(text_node)

    text = xml.createTextNode(CONST.SYSTEM_NAME)
    text_node.appendChild(text)

    with open(filename, 'wb') as f:
        f.write(xml.toprettyxml(encoding='utf-8'))
        f.close()


def read_xml(file_path):
    element_tree = ElementTree()
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        init(file_path)
        log.info("init file:{}".format(file_path))
    element_tree.parse(file_path)
    return element_tree


def write_xml(element_tree, file_path):
    element_tree.write(file_path, encoding="utf-8", xml_declaration=True)


def find_nodes(element_tree, node_path):
    """
    element/test:获取root/element 节点下的所有test节点
    获取指定节点下的所有节点
    """
    return element_tree.findall(node_path)


def create_node(tag, content, property_map: dict={}):
    """
    新增一级节点（根节点下的节点）
    :param tag: 节点名称
    :param content: 节点内容
    :param property_map: 节点属性字典
    :return: 节点对象
    """
    element = Element(tag, property_map)
    element.text = content
    return element


def del_node_by_tag_name(nodelist, tag):
    """
    删除指定父节点下的指定名称标签
    :param nodelist: 父节点
    :param tag: 需要删除的节点标签名
    :return:
    """
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag:
                parent_node.remove(child)


@contextmanager
def op_xml(file_path_: str=None, update=False):
    """
    1 读取xml文件
    2 获取element_tree
    3 写xml
    :return: element_tree
    """
    try:
        if not file_path_:
            file_path_ = "{}{}".format(CONST.PROJECT_PATH, CONST.DB_PATH)
        element_tree = read_xml(file_path_)
        yield element_tree
        if update:
            write_xml(element_tree, file_path_)
    except Exception as e:
        log.exception(e)


def get_node_content(first_level_node, file_path=None):
    """
    :param first_level_node: 节点名称
    :param file_path: xml路径
    :return:
    """
    content = None
    with op_xml(file_path) as element_tree:
        _nodes = find_nodes(element_tree, first_level_node)
        if _nodes:
            content = _nodes[0].text
    return content


def set_or_update(first_level_node, value: str, file_path=None):
    with op_xml(file_path, update=True) as element_tree:
        _nodes = find_nodes(element_tree, first_level_node)
        if _nodes:
            _nodes[0].text = str(value)
        else:
            element = create_node(first_level_node, str(value))
            root = element_tree.getroot()
            root.append(element)


def get_all_order():
    return get_node_content(CONST.ALL_ORDER)


def set_all_order(value):
    set_or_update(CONST.ALL_ORDER, value)


def get_download():
    return get_node_content(CONST.ALL_ORDER, file_path="{}{}".format(CONST.PROJECT_PATH, CONST.DOWNLOAD_PATH))


def set_download(value):
    set_or_update(CONST.DOWNLOAD, value, file_path="{}{}".format(CONST.PROJECT_PATH, CONST.DOWNLOAD_PATH))

