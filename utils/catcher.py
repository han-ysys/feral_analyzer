import requests
from utils import api
import argparse

def events_data(
    report_code,
    token,
    fight_ids=None,
    start=None,
    end=None,
    ability_id=None,
    event_type=None,
    death=None,
    difficulty=None,
    encounter_id=None,
    filter_expression=None,
    hostility_type=None,
    include_resources=None,
    kill_type=None,
    limit=None,
    source_auras_absent=None,
    source_auras_present=None,
    source_class=None,
    source_id=None,
    source_instance_id=None,
    target_auras_absent=None,
    target_auras_present=None,
    target_class=None,
    target_id=None,
    target_instance_id=None,
    translate=None,
    use_ability_ids=None,
    use_actor_ids=None,
    view_options=None,
    wipe_cutoff=None
):
    """
    Parameters:
    - abilityID: 指定技能的游戏ID, 用于筛选特定技能的事件。
    - dataType: 事件的数据类型, 如伤害、治疗、死亡等。
    - death: 若查询死亡事件, 可指定某次死亡编号。
    - difficulty: 筛选特定难度的战斗, 默认包含所有难度。
    - encounterID: 筛选特定Boss的战斗, 默认包含所有Boss。
    - endTime: 查询时间范围的结束时间(UNIX时间戳)。
    - fightIDs: 只包含指定战斗ID的事件, 其他将被排除。
    - filterExpression: 使用站点提供的查询语言自定义事件筛选条件。
    - hostilityType: 敌对类型(0表示友方视角, 1表示敌方视角)。
    - includeResources: 是否包含单位的详细资源信息(如法力、能量等), 默认关闭。
    - killType: 筛选击杀、灭团、Boss战或小怪战。
    - limit: 限制返回的事件数量(允许范围为100-10000, 默认300)。
    - sourceAurasAbsent: 来源单位必须缺失的光环(以逗号分隔)。
    - sourceAurasPresent: 来源单位必须拥有的光环(以逗号分隔)。
    - sourceClass: 来源单位的职业标识符(如'mage', 'priest')。
    - sourceID: 来源单位的ID。
    - sourceInstanceID: 来源单位的实例ID。
    - startTime: 查询时间范围的起始时间(UNIX时间戳)。
    - targetAurasAbsent: 目标单位必须缺失的光环(以逗号分隔)。
    - targetAurasPresent: 目标单位必须拥有的光环(以逗号分隔)。
    - targetClass: 目标单位的职业标识符。
    - targetID: 目标单位的ID。
    - targetInstanceID: 目标单位的实例ID。
    - translate: 是否自动翻译战斗数据(默认为True, 设为False可提高性能)。
    - useAbilityIDs: 是否包含技能的详细信息(默认True, 会增加带宽使用)。
    - useActorIDs: 是否包含角色的详细信息(默认True, 会增加带宽使用)。
    - viewOptions: 页面视图设置的位掩码, 可通过前端页面实验得出值。
    - wipeCutoff: 当战斗中死亡人数超过此值时, 忽略之后的事件。

    """
    query = """
    query (
      $code: String!,
      $startTime: Float,
      $endTime: Float,
      $abilityID: Float,
      $dataType: EventDataType,
      $death: Int,
      $difficulty: Int,
      $encounterID: Int,
      $fightIDs: [Int],
      $filterExpression: String,
      $hostilityType: HostilityType,
      $includeResources: Boolean,
      $killType: KillType,
      $limit: Int,
      $sourceAurasAbsent: String,
      $sourceAurasPresent: String,
      $sourceClass: String,
      $sourceID: Int,
      $sourceInstanceID: Int,
      $targetAurasAbsent: String,
      $targetAurasPresent: String,
      $targetClass: String,
      $targetID: Int,
      $targetInstanceID: Int,
      $translate: Boolean,
      $useAbilityIDs: Boolean,
      $useActorIDs: Boolean,
      $viewOptions: Int,
      $wipeCutoff: Int
    ) {
      reportData {
        report(code: $code) {
          events(
            startTime: $startTime,
            endTime: $endTime,
            abilityID: $abilityID,
            dataType: $dataType,
            death: $death,
            difficulty: $difficulty,
            encounterID: $encounterID,
            fightIDs: $fightIDs,
            filterExpression: $filterExpression,
            hostilityType: $hostilityType,
            includeResources: $includeResources,
            killType: $killType,
            limit: $limit,
            sourceAurasAbsent: $sourceAurasAbsent,
            sourceAurasPresent: $sourceAurasPresent,
            sourceClass: $sourceClass,
            sourceID: $sourceID,
            sourceInstanceID: $sourceInstanceID,
            targetAurasAbsent: $targetAurasAbsent,
            targetAurasPresent: $targetAurasPresent,
            targetClass: $targetClass,
            targetID: $targetID,
            targetInstanceID: $targetInstanceID,
            translate: $translate,
            useAbilityIDs: $useAbilityIDs,
            useActorIDs: $useActorIDs,
            viewOptions: $viewOptions,
            wipeCutoff: $wipeCutoff
          ) {
            data,
            nextPageTimestamp
          }
        }
      }
    }
    """

    variables = {
        "code": report_code,
        "startTime": start,
        "endTime": end,
        "abilityID": ability_id,
        "dataType": event_type,
        "death": death,
        "difficulty": difficulty,
        "encounterID": encounter_id,
        "fightIDs": fight_ids,
        "filterExpression": filter_expression,
        "hostilityType": hostility_type,
        "includeResources": include_resources,
        "killType": kill_type,
        "limit": limit,
        "sourceAurasAbsent": source_auras_absent,
        "sourceAurasPresent": source_auras_present,
        "sourceClass": source_class,
        "sourceID": source_id,
        "sourceInstanceID": source_instance_id,
        "targetAurasAbsent": target_auras_absent,
        "targetAurasPresent": target_auras_present,
        "targetClass": target_class,
        "targetID": target_id,
        "targetInstanceID": target_instance_id,
        "translate": translate,
        "useAbilityIDs": use_ability_ids,
        "useActorIDs": use_actor_ids,
        "viewOptions": view_options,
        "wipeCutoff": wipe_cutoff
    }
    # Remove None values to avoid sending them in the request
    variables = {k: v for k, v in variables.items() if v is not None}

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api.API_URL, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()['data']['reportData']['report']['events']
    nextPageTimestamp = data.get('nextPageTimestamp')
    if nextPageTimestamp is not None:
        nextPage_data = events_data(
            report_code,
            fight_ids=fight_ids,
            start=nextPageTimestamp,
            end=end,
            ability_id=ability_id,
            event_type=event_type,
            token=token,
            death=death,
            difficulty=difficulty,
            encounter_id=encounter_id,
            filter_expression=filter_expression,
            hostility_type=hostility_type,
            include_resources=include_resources,
            kill_type=kill_type,
            limit=limit,
            source_auras_absent=source_auras_absent,
            source_auras_present=source_auras_present,
            source_class=source_class,
            source_id=source_id,
            source_instance_id=source_instance_id,
            target_auras_absent=target_auras_absent,
            target_auras_present=target_auras_present,
            target_class=target_class,
            target_id=target_id,
            target_instance_id=target_instance_id,
            translate=translate,
            use_ability_ids=use_ability_ids,
            use_actor_ids=use_actor_ids,
            view_options=view_options,
            wipe_cutoff=wipe_cutoff
        )
        data['data'].extend(nextPage_data)
    return data['data']

def fights_data(report_code, token):
    query = """
    query ($code: String!) {
      reportData {
        report(code: $code) {
          fights {
            id
            startTime
            endTime
            kill
          }
        }
      }
    }
    """
    variables = {"code": report_code}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api.API_URL, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['data']['reportData']['report']

def spec_rankings(spec, _class, token):
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

def table_data(
  report_code,
  token,
  ability_id=None,
  data_type=None,
  death=None,
  difficulty=None,
  encounter_id=None,
  end=None,
  fight_ids=None,
  filter_expression=None,
  hostility_type=None,
  kill_type=None,
  source_auras_absent=None,
  source_auras_present=None,
  source_class=None,
  source_id=None,
  source_instance_id=None,
  start=None,
  target_auras_absent=None,
  target_auras_present=None,
  target_class=None,
  target_id=None,
  target_instance_id=None,
  translate=None,
  view_options=None,
  view_by=None,
  wipe_cutoff=None
):
  """
  Fetches table data for a report, filterable via various arguments.

  See function docstring for argument details.
  """
  query = """
  query (
    $code: String!,
    $abilityID: Float,
    $dataType: TableDataType,
    $death: Int,
    $difficulty: Int,
    $encounterID: Int,
    $endTime: Float,
    $fightIDs: [Int],
    $filterExpression: String,
    $hostilityType: HostilityType,
    $killType: KillType,
    $sourceAurasAbsent: String,
    $sourceAurasPresent: String,
    $sourceClass: String,
    $sourceID: Int,
    $sourceInstanceID: Int,
    $startTime: Float,
    $targetAurasAbsent: String,
    $targetAurasPresent: String,
    $targetClass: String,
    $targetID: Int,
    $targetInstanceID: Int,
    $translate: Boolean,
    $viewOptions: Int,
    $viewBy: ViewType,
    $wipeCutoff: Int
  ) {
    reportData {
    report(code: $code) {
      table(
      abilityID: $abilityID,
      dataType: $dataType,
      death: $death,
      difficulty: $difficulty,
      encounterID: $encounterID,
      endTime: $endTime,
      fightIDs: $fightIDs,
      filterExpression: $filterExpression,
      hostilityType: $hostilityType,
      killType: $killType,
      sourceAurasAbsent: $sourceAurasAbsent,
      sourceAurasPresent: $sourceAurasPresent,
      sourceClass: $sourceClass,
      sourceID: $sourceID,
      sourceInstanceID: $sourceInstanceID,
      startTime: $startTime,
      targetAurasAbsent: $targetAurasAbsent,
      targetAurasPresent: $targetAurasPresent,
      targetClass: $targetClass,
      targetID: $targetID,
      targetInstanceID: $targetInstanceID,
      translate: $translate,
      viewOptions: $viewOptions,
      viewBy: $viewBy,
      wipeCutoff: $wipeCutoff
      )
    }
    }
  }
  """

  variables = {
    "code": report_code,
    "abilityID": ability_id,
    "dataType": data_type,
    "death": death,
    "difficulty": difficulty,
    "encounterID": encounter_id,
    "endTime": end,
    "fightIDs": fight_ids,
    "filterExpression": filter_expression,
    "hostilityType": hostility_type,
    "killType": kill_type,
    "sourceAurasAbsent": source_auras_absent,
    "sourceAurasPresent": source_auras_present,
    "sourceClass": source_class,
    "sourceID": source_id,
    "sourceInstanceID": source_instance_id,
    "startTime": start,
    "targetAurasAbsent": target_auras_absent,
    "targetAurasPresent": target_auras_present,
    "targetClass": target_class,
    "targetID": target_id,
    "targetInstanceID": target_instance_id,
    "translate": translate,
    "viewOptions": view_options,
    "viewBy": view_by,
    "wipeCutoff": wipe_cutoff
  }
  variables = {k: v for k, v in variables.items() if v is not None}

  headers = {"Authorization": f"Bearer {token}"}
  response = requests.post(api.API_URL, json={'query': query, 'variables': variables}, headers=headers)
  response.raise_for_status()
  data = response.json()
  return data['data']['reportData']['report']['table']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch events data from a report.")
    parser.add_argument("-r", "--report_code", type=str, required=True, help="The report code to fetch data for.")
    parser.add_argument("-t", "--token", type=str, default=None, help="Access token for the API. If not provided, it will be fetched using the API client credentials.")
    args = parser.parse_args()

    token = api.get_access_token() if args.token is None else args.token

    events_data = fights_data(args.report_code, token)
    print(events_data)