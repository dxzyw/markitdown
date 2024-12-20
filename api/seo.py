from flask import Blueprint, make_response
from datetime import datetime
import xml.etree.ElementTree as ET

seo = Blueprint('seo', __name__)

@seo.route('/sitemap.xml')
def sitemap():
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # 添加主页
    url = ET.SubElement(root, 'url')
    ET.SubElement(url, 'loc').text = 'https://yourdomain.com/'
    ET.SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
    ET.SubElement(url, 'changefreq').text = 'daily'
    ET.SubElement(url, 'priority').text = '1.0'
    
    # 添加转换工具页面
    url = ET.SubElement(root, 'url')
    ET.SubElement(url, 'loc').text = 'https://yourdomain.com/markdown'
    ET.SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
    ET.SubElement(url, 'changefreq').text = 'weekly'
    ET.SubElement(url, 'priority').text = '0.8'
    
    response = make_response(ET.tostring(root, encoding='utf-8'))
    response.headers['Content-Type'] = 'application/xml'
    return response 