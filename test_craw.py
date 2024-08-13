from bs4 import BeautifulSoup
import json

html = '''
<div class="rno-learning-path-section">
    <h5 class="rno-learning-path-section-title" title="产品简介">产品简介</h5>
    <ul class="rno-learning-path-section-list list-3">
        <li><a hotrep="doc.overview.modules.path.0.0.0" href="https://cloud.tencent.com/document/product/1709/94945" title="什么是腾讯云向量数据库？">什么是腾讯云向量数据库？</a></li>
        <li><a hotrep="doc.overview.modules.path.0.0.1" href="https://cloud.tencent.com/document/product/1709/95010" title="设计架构">设计架构</a></li>
        <li><a hotrep="doc.overview.modules.path.0.0.2" href="https://cloud.tencent.com/document/product/1709/95428" title="索引与计算">索引与计算</a></li>
        <li><a hotrep="doc.overview.modules.path.0.0.3" href="https://cloud.tencent.com/document/product/1709/95099" title="检索方法">检索方法</a></li>
        <li><a hotrep="doc.overview.modules.path.0.0.4" href="https://cloud.tencent.com/document/product/1709/94946" title="产品优势">产品优势</a></li>
        <li><a hotrep="doc.overview.modules.path.0.0.5" href="https://cloud.tencent.com/document/product/1709/94947" title="应用场景">应用场景</a></li>
    </ul>
</div>
'''

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html, 'lxml')

# 选择所有的<a>标签
links = soup.select('div.rno-learning-path-section ul li a')

# 遍历并提取链接的href和title属性
for link in links:
    href = link.get('href')
    title = link.get('title')
    print(f"Title: {title}, URL: {href}")
