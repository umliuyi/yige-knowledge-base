# -*- coding: utf-8 -*-
"""PDF内容提取脚本"""
import os, sys

pdf_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\乐城先行区健康解决方案全览.pdf"
out_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\知识库\乐城先行区健康解决方案全览-20260513.md"

print(f"Reading PDF: {pdf_path}")
print(f"File size: {os.path.getsize(pdf_path)//1024} KB")

try:
    import pymupdf
    print("pymupdf imported OK")
except ImportError:
    print("pymupdf not available, trying fitz...")
    try:
        import fitz
        print("fitz OK")
    except ImportError:
        print("ERROR: no PDF library available")
        sys.exit(1)

# Read PDF
doc = pymupdf.open(pdf_path)
print(f"Pages: {doc.page_count}")

pages_text = []
for i, page in enumerate(doc):
    text = page.get_text("text")
    if text.strip():
        pages_text.append(f"## 第{i+1}页\n{text}")
    if (i+1) % 10 == 0:
        print(f"Read {i+1}/{doc.page_count} pages...")

doc.close()
print(f"Extracted text from {len(pages_text)} pages")

# Build markdown
lines = [
    "# 乐城先行区健康解决方案全览",
    "",
    "## 文件信息",
    f"- PDF页数：{len(pages_text)}页",
    f"- 来源：海南首位健康科技有限公司内部资料",
    "",
    "## 核心内容",
    "",
]
for pt in pages_text:
    lines.append(pt)
    lines.append("")

content = "\n".join(lines)
print(f"Total content: {len(content)} chars")

with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Written to: {out_path}")
print(f"File size: {os.path.getsize(out_path)//1024} KB")