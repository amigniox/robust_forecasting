## robust_forecasting
Application Load Forecasting Project@Insight
# Problem
The aim of this project is to take our current application load forecasting approach: 
1. Understand its accuracy and validity  across different types of workload
- Provide metrics and test tools as well as overall report.
2. Improve it so that its fairly accurate  across different workloads
- Push the current accuracy across workloads up so we can be fairly confident
about using it
3. Prove its robustness: 
- This means it works at different time resolutions (5s, 1m, 1h) and at different request scales ie. 1 Requests Per Second 100 Requests Per Second, 1e6 Requests Per Second, 1e10 Requests Per second.
4. Provide a  path forward  for further improvements: 
- Provide us with details on how to further improve including: What degree does
aggregation and time scale matter for forecasting. How can we further improve, etc.
