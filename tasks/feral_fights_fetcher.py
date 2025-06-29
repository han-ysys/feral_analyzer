import common_utils.api as api
import requests
import json

token = api.get_access_token()

def get_spec_rankings(spec, _class):
    query = """
    query ($id: Int!, $specName: String, $className: String) {
      worldData {
        zone (id: $id) {
            id,
            name,
            encounters {
              id,
              name,
              characterRankings (specName: $specName, className: $className, leaderboard: LogsOnly) 
            }
        }
      }
    }
    """
    variables = {"id": 43, "specName": spec, "className": _class}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api.API_URL, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data

def main():
    try:
        result = get_spec_rankings('Feral', 'Druid')
        with open('data_json/top_ferals.json', 'w') as f:
            json.dump(result, f, indent=4)
    except Exception as e:
        print(f"Error fetching dungeons: {e}")

if __name__ == "__main__":
    main()