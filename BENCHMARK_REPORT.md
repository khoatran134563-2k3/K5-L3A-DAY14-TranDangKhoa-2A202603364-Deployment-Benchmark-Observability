# Benchmark & Observability Report — Day 14

> Copy file này thành `BENCHMARK_REPORT.md` trong repo của bạn và điền đầy đủ.
> Mọi con số phải lấy từ report JSON / CSV / screenshot thật, không ước lượng.

**Họ tên:** ...
**Ngày chạy:** ...
**Môi trường:** (vd MacBook M2, Docker Desktop 4 CPU / 8GB RAM)

---

## 1. SLO của agent

| SLI | SLO | Lý do chọn ngưỡng này |
|---|---|---|
| p95 latency `/ask` | < ___ ms | |
| Error rate `/ask` | < ___ % | |
| Accuracy trên golden dataset | ≥ ___ % | |

---

## 2. Benchmark hiệu năng (develop, `load_test.py`)

### 2.1 Concurrency vs latency (agent v2)

| Concurrency | RPS | p50 (ms) | p95 (ms) | p99 (ms) | Error rate | SLO |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 10 | | | | | | |
| 50 | | | | | | |
| 100 | | | | | | |

**Nhận xét:** RPS có tăng tuyến tính theo concurrency không? Vì sao?

...

### 2.2 Tail latency

| `MOCK_SLOW_RATE` | avg (ms) | p95 (ms) | p99 (ms) |
|---|---|---|---|
| 0 | | | |
| 0.03 (mặc định) | | | |
| 0.1 | | | |

**Nhận xét:** Chỉ số nào nhạy nhất với request chậm? Vì sao SLO không nên đặt theo average?

...

---

## 3. Benchmark chất lượng (develop, `eval/run_eval.py`)

| Chỉ số | Agent v1 | Agent v2 | Agent v2 (sau khi sửa KB) |
|---|---|---|---|
| Accuracy | | | |
| Avg tokens / câu | | | |
| Tổng cost (USD) | | | |
| Cost / câu đúng (USD) | | | |
| Quality gate | PASS / FAIL | PASS / FAIL | PASS / FAIL |

**Những câu v2 trả lời sai ban đầu và cách bạn sửa:**

| ID | Keyword bị thiếu | Bạn đã sửa gì |
|---|---|---|
| | | |

**Nhận xét về trade-off chất lượng / chi phí / latency giữa v1 và v2:**

...

---

## 4. Observability stack (production)

### 4.1 Screenshot

- [x] [Grafana với lịch sử tải và 3 instance](screenshots/grafana-dashboard.png)
- [x] [Trace chậm](screenshots/jaeger-slow-trace.png)
- [x] [Trace lỗi 503](screenshots/jaeger-error-trace.png)
- [ ] [Ảnh Prometheus gốc](screenshots/prometheus-alert-firing.png) chụp lúc error đã firing và latency còn pending. [Lịch sử Prometheus](benchmark-results/chaos-prometheus-alerts.json) xác nhận hai alert cùng firing từ mẫu 23:32:20 (GMT+7).

### 4.2 Thí nghiệm "phá hệ thống"

| # | Thay đổi | Alert nào firing | Thời gian từ lúc đổi → firing | Panel nào phản ánh rõ nhất |
|---|---|---|---|---|
| A | `MOCK_ERROR_RATE=0.2` | `AgentHighErrorRate` | Mẫu đầu tiên 23:31:15, sau 68 giây từ lúc Locust bắt đầu | Error rate |
| B | `MOCK_SLOW_RATE=0.3` | `AgentHighLatencyP95` | Mẫu đầu tiên 23:32:20, sau 133 giây từ lúc Locust bắt đầu | Latency p95 |
| C | `LLM_MODEL=mock-llm-large` | | | |
| D | `docker pause` 1 instance | | | |
| E | `AGENT_VERSION=v1` | | | |

A và B chạy đồng thời. Locust bắt đầu lúc 23:30:07 theo `chaos_stats_history.csv`. Mẫu Prometheus có bước 5 giây. Trong lượt chaos, `/ask` lỗi 2.429/12.033 request (20,19%), tất cả là HTTP 503, và p95 là 1.700 ms. [CSV chaos](benchmark-results/chaos_stats.csv)

**Thí nghiệm E không làm alert nào firing. Bạn sẽ phát hiện loại sự cố này trong production bằng cách nào?**

...

### 4.3 Debug bằng trace

Chọn 1 trace chậm nhất bạn tìm được:

- `trace_id`: `e142e8b05907acc8ca311d3fa4d5b339`
- Tổng thời gian Jaeger: 1.741,78 ms
- Span con `chat mock-llm-small`: 1.721,74 ms (98,85%). Trường `llm_ms` trong log là độ trễ riêng do mock báo về.
- Dòng log tương ứng (grep theo `trace_id`):

```json
{"ts": "2026-11-25T16:34:06.698634+00:00", "level": "INFO", "service": "observable-agent", "instance": "9ef3ffd2e6fc", "event": "llm_call", "trace_id": "e142e8b05907acc8ca311d3fa4d5b339", "span_id": "6f07acbade52975f", "request_id": "c0fbf31ca65d", "model": "mock-llm-small", "agent_version": "v2", "input_tokens": 83, "output_tokens": 44, "cost_usd": 3.9e-05, "llm_ms": 1667.8}
```

Trace lỗi `d030509805639bf6052b9a5173cbd210` trả 503 sau 890,58 ms. Span `chat mock-llm-small` mất 860,84 ms và chứa event `exception` với `error.type=upstream_unavailable`.

```json
{"ts": "2026-11-25T16:34:06.694210+00:00", "level": "INFO", "service": "observable-agent", "instance": "2f82a692de0a", "event": "llm_error", "trace_id": "d030509805639bf6052b9a5173cbd210", "span_id": "9f780eb8e4dd4367", "request_id": "b9a0d774c332", "error": "Upstream LLM error: 503 Service Unavailable (mock)"}
```

---

## 5. Benchmark scaling (production, Locust headless, 100 users, 2 phút)

| Số instance | Requests | RPS | Mean (ms) | p50 (ms) | p95 (ms) | p99 (ms) | Failures | Error rate |
|---|---|---|---|---|---|---|---|---|
| 1 | 7.852 | 65,6808 | 224,1627 | 190 | 310 | 1.700 | 67 | 0,85% |
| 3 | 7.859 | 65,6849 | 213,8482 | 190 | 230 | 1.700 | 84 | 1,07% |

Số liệu từ dòng `Aggregated` trong [scale_1_stats.csv](benchmark-results/scale_1_stats.csv) và [scale_3_stats.csv](benchmark-results/scale_3_stats.csv). Dòng `POST /ask` riêng có p95 lần lượt là 340 và 230 ms, với 67/7.143 và 84/7.145 request lỗi. Cả hai lượt ghi nhận mọi failure là HTTP 503 ở `POST /ask`.

**Giải thích kết quả:** Scale có cải thiện p95 không? Nút thắt nằm ở đâu?

...

---

## 6. Kết luận

- 3 điều bạn học được về benchmark & observability:
  1. ...
  2. ...
  3. ...
- Nếu đưa agent này lên production thật, bạn sẽ thêm metric / alert nào nữa?

...
