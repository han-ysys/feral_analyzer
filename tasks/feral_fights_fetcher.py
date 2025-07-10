import utils.api as api
import json
import time

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
    variables = {
      "id": 43, # TWW season 2
      "specName": spec, 
      "className": _class
    }
    data = api.send_request(query, variables)
    return data

def main():
    try:
        result = get_spec_rankings('Feral', 'Druid')
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        with open(f'data_json/top_ferals_{timestamp}.json', 'w') as f:
            json.dump(result, f, indent=4)
    except Exception as e:
        print(f"Error fetching ranking: {e}")

if __name__ == "__main__":
    main()