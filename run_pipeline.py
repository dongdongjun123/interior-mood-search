# 전체 무드 라이브러리 파이프라인 일괄 실행
from __future__ import annotations  # 타입 힌트 forward reference 지원

import argparse  # CLI 옵션 (--k, --no-dedup, --skip-viz)

from mood_pipeline.build_library import run_build_library  # mood_library 생성
from mood_pipeline.cluster import load_embeddings_and_paths, plot_elbow, plot_umap, run_clustering  # 클러스터링
from mood_pipeline.embed import run_embedding  # CLIP 임베딩
from mood_pipeline.label import run_labeling  # 무드 라벨링
from mood_pipeline.preprocess import prepare_dataset  # 데이터 준비


def main():
    parser = argparse.ArgumentParser(description="무드 라이브러리 파이프라인")
    parser.add_argument("--k", type=int, default=None, help="클러스터 수 (미지정 시 자동)")
    parser.add_argument("--no-dedup", action="store_true", help="시각적 중복 제거 비활성화")
    parser.add_argument("--skip-viz", action="store_true", help="UMAP/elbow 시각화 생략")
    args = parser.parse_args()  # 터미널 인자 파싱

    print("=== 데이터 준비 ===")
    manifest = prepare_dataset()  # image_paths.json 생성
    print(f"  이미지 {manifest['count']}장")

    print("=== CLIP 임베딩 ===")
    emb_result = run_embedding(deduplicate=not args.no_dedup)  # embeddings.npy
    print(f"  {emb_result['shape']}, device={emb_result['device']}")

    print("=== 클러스터링 ===")
    cluster_result = run_clustering(n_clusters=args.k)  # clusters.json
    print(f"  k={cluster_result['n_clusters']}, sizes={cluster_result['cluster_sizes']}")

    if not args.skip_viz:
        emb, _ = load_embeddings_and_paths()
        import numpy as np

        labels = np.load("data/cluster_labels.npy")
        plot_umap(emb, labels)   # 2D 분포 PNG
        plot_elbow(emb)          # elbow curve PNG
        print("  시각화 → data/previews/")

    print("=== 라벨링 ===")
    label_result = run_labeling()  # labels.json, metadata.csv
    print(f"  {label_result['n_clusters']} clusters, montages={len(label_result['montages'])}")

    print("=== 무드 라이브러리 ===")
    lib_result = run_build_library()  # mood_library/
    print(f"  {lib_result['mood_count']} moods → {lib_result['library_path']}")

    print("\n완료!")


if __name__ == "__main__":
    main()
