# 프롬pt → mood_library 검색 (노트북 없이 터미널 테스트용)
from __future__ import annotations

import argparse
import json

from mood_pipeline.search import (
    plot_search_result,
    prepare_prompt_for_search,
    search_mood_by_prompt,
    search_mood_with_images,
)


def main():
    parser = argparse.ArgumentParser(description="프롬프트 기반 무드 검색")
    parser.add_argument("prompt", help="검색할 프롬프트 문장")
    parser.add_argument("--top-k", type=int, default=2, help="추천 gallery 이미지 개수 (무드만 검색 시 후보 무드 개수)")
    parser.add_argument("--moods-only", action="store_true", help="1차 무드 검색만")
    parser.add_argument("--plot", action="store_true", help="matplotlib figure 표시")
    parser.add_argument("--no-translate", action="store_true", help="한→영 번역 비활성화")
    args = parser.parse_args()

    translate_ko = not args.no_translate

    if args.moods_only:
        prepared = prepare_prompt_for_search(args.prompt, translate_ko=translate_ko)
        moods = search_mood_by_prompt(
            args.prompt,
            top_k=args.top_k,
            translate_ko=translate_ko,
            prepared=prepared,
        )
        if translate_ko:
            result = {
                "prompt_original": prepared["prompt_original"],
                "prompt_en": prepared["prompt_en"],
                "translated": prepared["translated"],
                "moods": moods,
            }
        else:
            result = moods
    else:
        result = search_mood_with_images(
            args.prompt,
            top_k=args.top_k,
            translate_ko=translate_ko,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.plot and isinstance(result, dict):
        display_prompt = result.get("prompt_en", args.prompt)
        plot_search_result(result, prompt=display_prompt)


if __name__ == "__main__":
    main()
