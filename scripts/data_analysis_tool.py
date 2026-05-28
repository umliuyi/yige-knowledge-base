#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析 + 图表生成工具
支持 CSV/Excel 文件读取、基础分析、图表生成、报告输出
"""

import argparse
import os
import sys
from datetime import datetime

import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np

# ============================================================
# 中文字体配置
# ============================================================
def setup_chinese_font():
    """配置中文字体支持"""
    # 尝试多种中文字体
    font_candidates = [
        'Microsoft YaHei',
        'SimHei',
        'PingFang SC',
        'STHeiti',
        'WenQuanYi Micro Hei',
        'Noto Sans CJK SC',
        'Source Han Sans CN',
    ]
    
    found_font = None
    for font in font_candidates:
        if font in [f.name for f in fm.fontManager.ttflist]:
            found_font = font
            break
    
    if found_font:
        plt.rcParams['font.sans-serif'] = [found_font]
        print(f"[INFO] 使用字体: {found_font}")
    else:
        print("[WARNING] 未找到中文字体，图表中文可能显示异常")
    
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# ============================================================
# 数据读取
# ============================================================
def read_data(file_path):
    """读取 CSV 或 Excel 文件"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.csv':
        # 尝试不同编码
        for encoding in ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']:
            try:
                return pd.read_csv(file_path, encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"无法以已知编码读取 CSV 文件: {file_path}")
    
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    
    else:
        raise ValueError(f"不支持的文件格式: {ext}，仅支持 .csv 和 .xlsx")


# ============================================================
# 数据分析
# ============================================================
def analyze_data(df):
    """执行基础数据分析，返回分析结果字典"""
    results = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'numeric_summary': {},
        'text_summary': {},
        'growth_rates': {},
        'missing_values': df.isnull().sum().to_dict(),
    }
    
    # 数值列分析
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        results['numeric_summary'][col] = {
            '总计': float(df[col].sum()),
            '平均值': float(df[col].mean()),
            '中位数': float(df[col].median()),
            '最大值': float(df[col].max()),
            '最小值': float(df[col].min()),
            '标准差': float(df[col].std()),
            '非空数量': int(df[col].count()),
        }
        
        # 增长率（假设数据按顺序排列）
        if len(df[col]) > 1:
            first_val = df[col].iloc[0]
            last_val = df[col].iloc[-1]
            if first_val != 0:
                growth = (last_val - first_val) / abs(first_val) * 100
                results['growth_rates'][col] = round(growth, 2)
    
    # 文本列分析
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        results['text_summary'][col] = {
            '唯一值数量': int(df[col].nunique()),
            '最常见值': df[col].mode().tolist()[:5],
            '非空数量': int(df[col].count()),
        }
    
    return results


# ============================================================
# 图表生成
# ============================================================
def generate_charts(df, analysis, output_dir):
    """生成并保存图表"""
    os.makedirs(output_dir, exist_ok=True)
    chart_files = []
    
    numeric_cols = list(analysis['numeric_summary'].keys())
    
    # 1. 数值列折线图
    if numeric_cols:
        fig, ax = plt.subplots(figsize=(12, 6))
        for col in numeric_cols[:5]:  # 最多5条线
            ax.plot(df.index, df[col], marker='o', label=col, linewidth=2)
        ax.set_title('数值列趋势图', fontsize=16)
        ax.set_xlabel('索引', fontsize=12)
        ax.set_ylabel('数值', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        path = os.path.join(output_dir, 'line_chart.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        chart_files.append(('折线图', path))
        print(f"[OK] 折线图已保存: {path}")
    
    # 2. 数值列柱状图
    if numeric_cols:
        fig, ax = plt.subplots(figsize=(12, 6))
        means = [analysis['numeric_summary'][col]['平均值'] for col in numeric_cols]
        colors = plt.cm.Set3(range(len(numeric_cols)))
        bars = ax.bar(numeric_cols, means, color=colors, edgecolor='black', linewidth=0.5)
        ax.set_title('数值列平均值对比', fontsize=16)
        ax.set_xlabel('列名', fontsize=12)
        ax.set_ylabel('平均值', fontsize=12)
        # 在柱子上显示数值
        for bar, val in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                   f'{val:.2f}', ha='center', va='bottom', fontsize=9)
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
        path = os.path.join(output_dir, 'bar_chart.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        chart_files.append(('柱状图', path))
        print(f"[OK] 柱状图已保存: {path}")
    
    # 3. 饼图 - 显示数值列的占比
    if numeric_cols:
        fig, ax = plt.subplots(figsize=(10, 8))
        sums = [analysis['numeric_summary'][col]['总计'] for col in numeric_cols]
        # 只显示前8个，其余合并
        if len(numeric_cols) > 8:
            top_cols = numeric_cols[:7]
            top_sums = sums[:7]
            other_sum = sum(sums[7:])
            top_cols.append('其他')
            top_sums.append(other_sum)
            labels = top_cols
            sizes = top_sums
        else:
            labels = numeric_cols
            sizes = sums
        
        colors = plt.cm.Pastel1(range(len(labels)))
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90,
            wedgeprops=dict(edgecolor='black', linewidth=0.5)
        )
        ax.set_title('数值列总计占比', fontsize=16)
        path = os.path.join(output_dir, 'pie_chart.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        chart_files.append(('饼图', path))
        print(f"[OK] 饼图已保存: {path}")
    
    # 4. 数值分布箱线图
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots(figsize=(12, 6))
        data_to_plot = [df[col].dropna().values for col in numeric_cols[:5]]
        bp = ax.boxplot(data_to_plot, labels=numeric_cols[:5], patch_artist=True)
        colors = plt.cm.Set3(range(len(data_to_plot)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        ax.set_title('数值列分布（箱线图）', fontsize=16)
        ax.set_ylabel('数值', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        path = os.path.join(output_dir, 'boxplot.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        chart_files.append(('箱线图', path))
        print(f"[OK] 箱线图已保存: {path}")
    
    return chart_files


# ============================================================
# 报告生成
# ============================================================
def generate_report(df, analysis, chart_files, output_dir):
    """生成文字分析报告"""
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("                   数据分析报告")
    report_lines.append("=" * 60)
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # 基本信息
    report_lines.append("【1. 数据概览】")
    report_lines.append(f"  - 文件: {df.shape[0]} 行 × {df.shape[1]} 列")
    report_lines.append(f"  - 列名: {', '.join(analysis['columns'])}")
    report_lines.append(f"  - 内存占用: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    report_lines.append("")
    
    # 缺失值
    report_lines.append("【2. 数据质量】")
    for col, count in analysis['missing_values'].items():
        if count > 0:
            pct = count / analysis['row_count'] * 100
            report_lines.append(f"  - {col}: {count} 个缺失值 ({pct:.1f}%)")
    if not any(analysis['missing_values'].values()):
        report_lines.append("  - 无缺失值 ✓")
    report_lines.append("")
    
    # 数值列分析
    if analysis['numeric_summary']:
        report_lines.append("【3. 数值列统计】")
        for col, stats in analysis['numeric_summary'].items():
            report_lines.append(f"  ▶ {col}")
            report_lines.append(f"    总计: {stats['总计']:,.2f}  |  平均: {stats['平均值']:,.2f}  |  中位数: {stats['中位数']:,.2f}")
            report_lines.append(f"    最大: {stats['最大值']:,.2f}  |  最小: {stats['最小值']:,.2f}  |  标准差: {stats['标准差']:,.2f}")
            if col in analysis['growth_rates']:
                gr = analysis['growth_rates'][col]
                trend = "↑" if gr > 0 else "↓"
                report_lines.append(f"    增长率: {trend} {abs(gr):.2f}%")
            report_lines.append("")
    
    # 文本列分析
    if analysis['text_summary']:
        report_lines.append("【4. 文本列统计】")
        for col, stats in analysis['text_summary'].items():
            report_lines.append(f"  ▶ {col}")
            report_lines.append(f"    唯一值: {stats['唯一值数量']}  |  非空: {stats['非空数量']}")
            report_lines.append(f"    常见值: {', '.join(str(v) for v in stats['最常见值'][:3])}")
            report_lines.append("")
    
    # 生成的图表
    report_lines.append("【5. 生成的图表】")
    for chart_type, path in chart_files:
        report_lines.append(f"  - {chart_type}: {os.path.basename(path)}")
    report_lines.append("")
    
    report_lines.append("=" * 60)
    report_lines.append("                     报告结束")
    report_lines.append("=" * 60)
    
    report_text = '\n'.join(report_lines)
    
    # 保存报告
    report_path = os.path.join(output_dir, 'analysis_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"[OK] 分析报告已保存: {report_path}")
    return report_text, report_path


# ============================================================
# 主函数
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='数据分析 + 图表生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python data_analysis_tool.py -i data.csv -o ./output
  python data_analysis_tool.py -i sales.xlsx -o ./reports
  python data_analysis_tool.py -i data.csv -o ./output --encoding gbk
        """
    )
    parser.add_argument('-i', '--input', required=True, help='输入文件路径 (CSV 或 Excel)')
    parser.add_argument('-o', '--output', default='./output', help='输出目录 (默认: ./output)')
    parser.add_argument('--encoding', default='utf-8', help='CSV 文件编码 (默认: utf-8)')
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"[ERROR] 文件不存在: {args.input}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("           数据分析 + 图表生成工具")
    print(f"{'='*60}")
    print(f"[INFO] 输入文件: {args.input}")
    print(f"[INFO] 输出目录: {args.output}")
    print()
    
    # 配置字体
    setup_chinese_font()
    
    # 1. 读取数据
    print("[INFO] 正在读取数据...")
    try:
        df = read_data(args.input)
        print(f"[OK] 读取成功: {df.shape[0]} 行 × {df.shape[1]} 列")
        print(f"[INFO] 列名: {list(df.columns)}\n")
    except Exception as e:
        print(f"[ERROR] 读取文件失败: {e}")
        sys.exit(1)
    
    # 2. 分析数据
    print("[INFO] 正在分析数据...")
    analysis = analyze_data(df)
    print(f"[OK] 分析完成\n")
    
    # 3. 生成图表
    print("[INFO] 正在生成图表...")
    chart_files = generate_charts(df, analysis, args.output)
    print()
    
    # 4. 生成报告
    print("[INFO] 正在生成报告...")
    report_text, report_path = generate_report(df, analysis, chart_files, args.output)
    print()
    
    # 输出报告到控制台
    print(report_text)
    
    print(f"\n[SUCCESS] 分析完成！结果保存在: {os.path.abspath(args.output)}")


if __name__ == '__main__':
    main()