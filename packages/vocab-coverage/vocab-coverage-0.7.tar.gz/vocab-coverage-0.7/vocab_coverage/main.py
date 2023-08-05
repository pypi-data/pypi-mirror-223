# -*- coding: utf-8 -*-

import logging
import os
import sys
import argparse
import json
from dotenv import load_dotenv

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vocab_coverage import coverage_analysis, embedding_analysis
from vocab_coverage.utils import logger

def main():
    parser = argparse.ArgumentParser()

    subcommands = parser.add_subparsers(dest='command')

    cmdCoverage = subcommands.add_parser('coverage', help='模型汉字识字率分析')
    cmdCoverage.add_argument("--model_name", type=str, default="shibing624/text2vec-base-chinese", help="模型在 HuggingFace Hub 上的名称（默认为 shibing624/text2vec-base-chinese）")
    cmdCoverage.add_argument("--charset_file", type=str, default="", help="用以统计识字率的字表文件（默认为内置字符集文件）")
    cmdCoverage.add_argument("--output_dir", type=str, default="images", help="生成的图像文件的输出目录（默认为 images/assets）")
    cmdCoverage.add_argument("--debug", action='store_true', help="是否打印调试信息")

    cmdEmbedding = subcommands.add_parser('embedding', help='词向量可视化分析')
    cmdEmbedding.add_argument("--model_name", type=str, default="shibing624/text2vec-base-chinese", help="模型在 HuggingFace Hub 上的名称（默认为 shibing624/text2vec-base-chinese）")
    cmdEmbedding.add_argument("--charset_file", type=str, default="", help="用以统计识字率的字表文件（默认为内置字符集文件）")
    cmdEmbedding.add_argument("--output_dir", type=str, default="images", help="生成的图像文件的输出目录（默认为 images/assets）")
    cmdEmbedding.add_argument("--postfix", type=str, default=None, help="图像文件名可选后缀，用以控制生成的文件名")
    cmdEmbedding.add_argument("--flat", action='store_true', help="控制是否将图像文件直接输出到 output_dir 目录下（默认为 False）") 
    cmdEmbedding.add_argument("--override", action='store_true', help="是否覆盖已存在的图像文件（默认为 False）")
    cmdEmbedding.add_argument("--is_detailed", action='store_true', help="是否对汉字进行详细分类（默认为 False）")
    cmdEmbedding.add_argument("--debug", action='store_true', help="是否打印调试信息（默认为 False）")
    cmdEmbedding.add_argument("--skip_input_embeddings", action='store_true', help="不计算输入层的词向量")
    cmdEmbedding.add_argument("--output_embeddings", action='store_true', help="计算输出层的词向量")
    cmdEmbedding.add_argument("--reducer_method", type=str, default="tsne", help="降维算法（默认为 tsne），可选值为 tsne, umap, tsne_cuml, umap_cuml, umap_tsne, umap_tsne_cuml")
    cmdCharset = subcommands.add_parser('charset', help='生成用以统计识字率的字表文件')
    cmdCharset.add_argument("--charset_file", type=str, default="", help="用以统计识字率的字表文件（默认为内置字符集文件）")

    args = parser.parse_args()

    # if hasattr(args, "debug") and args.debug:
    #     logger.setLevel(logging.DEBUG)

    if len(args.charset_file) == 0:
        # 使用内置字符集文件
        charset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charsets.json')

    if args.command == 'charsets':
        from vocab_coverage import generate_charsets
        if len(args.charset_file) == 0:
            logger.error(f'请指定 --charset_file 参数')
            exit(1)
        generate_charsets(args.charset_file)
        return
    elif args.command == 'coverage':
        charsets = json.load(open(charset_file, 'r'))
        coverage_analysis(args.model_name, charsets, args.output_dir, args.debug)
        return
    elif args.command == 'embedding':
        charsets = json.load(open(charset_file, 'r'))
        etypes = []
        if not args.skip_input_embeddings:
            etypes.append('input')
        if args.output_embeddings:
            etypes.append('output')
        embedding_analysis(
            model_name=args.model_name,
            charsets=charsets,
            output_dir=args.output_dir,
            postfix=args.postfix,
            flat=args.flat,
            override=args.override,
            embedding_type=etypes,
            is_detailed=args.is_detailed,
            reducer_method=args.reducer_method,
            debug=args.debug)
    else:
        parser.print_help()
        return

if __name__ == "__main__":
    load_dotenv()
    main()
