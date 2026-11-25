# Day 14 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. [Your answer]
2. [Your answer]
...

### Exercise 1.2: Develop agent output

[Paste your request and response.]

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config  | ...     | ...        | ...            |
...

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: [Your answer]
2. Working directory: [Your answer]
...

### Exercise 2.3: Image size comparison
- Develop: [X] MB
- Production: [Y] MB
- Difference: [Z]%

### Exercises 2.2 and 2.4: Container and Compose verification

[Paste your container test result, service diagram, and Nginx test result.]

## Part 3: Cloud Deployment

### Exercise 3.1 or 3.2: Cloud deployment
- URL: [Your public URL]
- Screenshot: [Link to screenshot in repo]

### Railway and Render configuration comparison

[Add your comparison.]

### Exercise 3.3: Cloud Run pipeline

[Describe the pipeline in 3–5 lines.]

## Part 4: API Security

### Exercise 4.1-4.3: Test results
[Paste your test outputs]

### Exercise 4.4: Cost guard implementation
[Explain your approach]

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
[Your explanations and test results]

## Part 6 — Production readiness

[Paste your own full-check output]

## AI log

[Record what you asked, what AI suggested, and what you changed and verified.]

- Codex reviewed the K5 requirements, checked Docker and WSL availability, ran the initial static diagnostic, and prepared blank report templates. Student changes and verification: [complete after your own work].
- Codex reviewed the partial config diff, installed the benchmark dependencies in the WSL virtual environment, built the observability agent image, and ran the Prometheus alert rule unit tests. Student implementation and personal verification: [complete after your own work].
- Codex diagnosed the CP8 sample container startup error, added PYTHONUSERBASE to its Dockerfile, rebuilt it, and confirmed the local agent health endpoint through Nginx. Benchmark measurements and screenshots: [record your own run].
- The student ran both Locust scaling benchmarks and captured Grafana. Codex checked the CSVs and application logs, copied the original evidence to submission folders, transcribed the verified Locust measurements, and started the two CP7 agents. Codex suggested the documented fault injection settings for the student to run.

- Codex inspected the four student screenshots, matched both Jaeger traces to Docker JSON logs, exported Prometheus firing history from the student chaos run, and recorded the verified CP8 measurements. Codex ran separate diagnostics: CP5 static 0/12 and CP7 v2 21/23. These diagnostics are not student benchmark submissions.
\
- Codex re-ran the CP5 static checker on the current source (0/12 criteria, 6/24 static subchecks), verified both CP7 health endpoints, and sent a diagnostic POST to the CP1 sample (HTTP success). The student still needs to record their own exercise output.\
