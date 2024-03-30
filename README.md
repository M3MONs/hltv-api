# hltv-api
An unofficial python flask api for popular CS2 website hltv.org.

# Examples 
## Top teams
```python
@app.route("/top_teams", methods=["GET"])
```
![image](https://github.com/M3MONs/hltv-api/assets/67465063/d9c56b83-4037-40f6-94ff-67f4d6df7be1)

## Team
```python
@app.route("/team/<name>", methods=["GET"])
```
![image](https://github.com/M3MONs/hltv-api/assets/67465063/b240e586-f116-4e47-bb83-8cbbcbdf7296)

## Results
```python
@app.route("/results", methods=["GET"])
```
![image](https://github.com/M3MONs/hltv-api/assets/67465063/fc70a2ad-f872-4609-a957-d4ada8fc03a0)

## Upcoming matches
```python
@app.route("/upcoming_matches", methods=["GET"])
```
![image](https://github.com/M3MONs/hltv-api/assets/67465063/df278720-4ba6-4375-8676-711cf517de78)
