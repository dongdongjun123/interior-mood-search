# 무드 라이브러리 파이프라인 — 완료 현황

원룸 인테리어 이미지를 CLIP으로 분석해 **무드(mood) 단위 라이브러리**를 만들고, **자연어 프롬프트로 무드·이미지를 추천**하는 파이프라인입니다.

---

## 목표 아키텍처

```
프롬프트 → 라이브러리 유사 이미지 선택 → 프롬프트 재구성 → 새 이미지 생성
              ✅ 완료                      ❌ 미구현        ❌ 미구현
```

현재 **1단계(라이브러리 유사 이미지 선택)** 까지 구현·실행 완료.

---

## 데이터

| 항목 | 내용 |
|------|------|
| 입력 이미지 | `images/final/` |
| 총 이미지 수 | **361장** (중복 제거 후) |
| 무드 수 | **8개** |
| CLIP 모델 | `openai/clip-vit-base-patch32` (512-d) |
| 수집 소스 | 오늘의집, Pinterest 크롤러 |

---

## 완료된 8개 무드

| mood_id | 이름 | 이미지 수 |
|---------|------|-----------|
| `natural_wood` | 내추럴 우드 | 62 |
| `minimal_white` | 미니멀 화이트 | 50 |
| `bright_airy` | 밝은 에어리 | 22 |
| `cute_pastel` | 파스텔 귀여운 | 65 |
| `monochrome_minimal` | 모노톤 미니멀 | 48 |
| `vintage_retro` | 빈티지 레트로 | 55 |
| `warm_cozy` | 따뜻한 코지 원룸 | 42 |
| `luxury_modern` | 럭셔리 모던 | 17 |

---

## 완료된 파이프라인 (Phase 0~6)

| Phase | 내용 | 산출물 |
|-------|------|--------|
| 0 | 이미지 수집·검증·manifest | `data/image_paths.json` |
| 1 | CLIP 이미지 임베딩 | `data/embeddings.npy` |
| 2 | KMeans 클러스터링 (k 자동 선택) | `data/clusters.json`, UMAP/elbow 시각화 |
| 3 | CLIP zero-shot 무드 라벨링 (중복 무드 방지) | `data/labels.json`, `data/metadata.csv` |
| 4 | 무드 라이브러리 빌드 | `mood_library/` (cover, gallery, meta.json, index.json) |
| 5 | 검색 인덱스 빌드 | `mood_text_embeddings.npy`, `mood_rep_image_embeddings.npy` |
| 6 | 프롬프트 기반 무드·이미지 검색 | `search.py`, `05_search_mood.ipynb` |

---

## 구현된 코드

```
mood_pipeline/
├── config.py          # 경로·설정
├── preprocess.py      # 데이터 준비
├── embed.py           # CLIP 이미지·텍스트 임베딩
├── cluster.py         # KMeans, UMAP, elbow
├── label.py           # zero-shot 라벨링
├── build_library.py   # mood_library 생성
└── search.py          # 프롬프트 검색 + figure 시각화

notebooks/
├── 01_clip_embed.ipynb
├── 02_cluster.ipynb
├── 03_label.ipynb
├── 04_build_library.ipynb
└── 05_search_mood.ipynb

run_pipeline.py        # 전체 파이프라인 일괄 실행
search_mood.py         # 터미널 검색 CLI
```

---

## 검색 동작 방식

1. **1차 검색** — 사용자 프롬프트 → CLIP text embedding → 무드 meta 텍스트와 코사인 유사도 → Top-K 무드
2. **2차 검색** — 1위 무드 내 대표 이미지 ↔ 프롬프트 임베딩 코사인 유사도 → Top-K 이미지
3. **시각화** — `plot_search_result()` 로 cover·추천 gallery 이미지를 matplotlib figure로 표시

**예시 프롬프트**
```
따뜻하고 우드톤이 있는 아늑한 원룸
```

**실행 방법**
```powershell
# 노트북
notebooks/05_search_mood.ipynb  (셀 2 → 3 순서 실행)

# 터미널
python search_mood.py "따뜻하고 우드톤이 있는 아늑한 원룸" --plot
python mood_pipeline/search.py "warm cozy room" --plot
```

---

## 아직 미구현

- 프롬프트 재구성 (선택 무드·이미지 → 생성용 프롬프트)
- 새 이미지 생성 (Stable Diffusion / FLUX 등)
- 검색 세션 JSON 저장 (`prompt_session.json`)
- 검색 정확도 개선 (한국어 키워드 보강, meta 텍스트 확장)

---

## 참고 문서

상세 가이드: `MOOD_LIBRARY_PIPELINE.md`
