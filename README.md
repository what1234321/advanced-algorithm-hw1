# 과제 1. Compare sorting

장다혜 · 2025193117 · 지능형반도체공학과

GitHub: https://github.com/what1234321/advanced-algorithm-hw1.git

수업에서 배운 **삽입·병합 정렬**과 새로 학습한 **힙 정렬**을 비교합니다.
교수님의 `lec-algorithm/algorithm-env` 템플릿에서 컨테이너·VS Code 설정과 Makefile 구조를 가져왔습니다. 기존 버블 예제를 본 과제의 C/Python 구현으로 교체했습니다.

## 실행

Python 3.10 이상, C17 컴파일러, make가 필요합니다. 코드와 SVG 생성기는 외부 라이브러리를 사용하지 않습니다.

```sh
make test
make run
make charts
```

`make run`은 Python 실험을 먼저 실행하여 고정 시드의 입력 파일을 저장합니다. C 실험은 바로 그 입력을 읽습니다. C만 실행하려면 입력을 먼저 생성하세요.

```sh
make run-py
make run-c
```

- 크기: 100, 1000, 2000, 4000
- 입력: 정렬, 역순, 무작위 순열, 중복많음(0~9)
- 각 조건 5회 실행의 시간 중앙값(ms)
- 입력 복사·검증·파일 입출력은 정렬 시간에서 제외
- 키 비교만 계수, 인덱스 조건은 제외
- Python 시간: `perf_counter_ns()`의 벽시계 시간
- C 시간: `clock()`의 CPU 시간
- 언어별 시간은 별도로 해석하고, C/Python 사이에는 키 비교 횟수가 일치하는지 자동 확인

## 구성

- `src/sort.py`, `src/sort.c`, `src/sort.h`: 정렬 구현과 공통 호출 표
- `src/main.py`, `src/main.c`: 실험 및 정답 검증
- `tests/test_sort.py`, `tests/test_sort.c`: 경계값·중복·안정성·크기별 테스트
- `results/benchmark.csv`, `results/benchmark_c.csv`: 실측값
- `results/inputs/`: 두 언어가 공유하는 실험 입력
- `tools/plot.py`: CSV로 SVG 생성
- `report/REPORT.pdf`: 제출용 한글 보고서
- `report/growth.svg`: 입력 크기에 따른 비교 횟수 그래프
- 컨테이너 및 VS Code 설정: 수업 템플릿에서 가져옴

공간복잡도는 구현 구조로 분석했으며, 실제 메모리 사용량은 측정하지 않았습니다. Docker/Codespaces 설정은 포함되어 있지만, 이번 검증은 Linux 호스트의 gcc와 Python으로 진행했습니다.

## 제출

이 파일들을 GitHub 저장소에 업로드한 뒤, 해당 저장소의 `Code > Download ZIP`으로 받은 ZIP과 보고서 PDF를 제출하세요.
