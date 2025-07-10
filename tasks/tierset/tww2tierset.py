# this is a python version copy from wowanalyzer, not usable

from parser.core.analyzer import Analyzer, SELECTED_PLAYER
from parser.core.module import Options
from game.tiers import TIERS
from common.spells.spell import Spell
from parser.core.events import Events, DamageEvent
from parser.shared.modules.damage_value import effective_damage
from common import SPELLS
from parser.core.event_calculate_lib import calculate_effective_damage
from common.items.dragonflight import DRUID_TWW2_ID
from parser.ui.statistic_category import STATISTIC_CATEGORY
from parser.ui.statistic_box import STATISTIC_ORDER
from parser.ui.statistic import Statistic
from parser.ui.item_percent_damage_done import ItemPercentDamageDone
from common.talents import TALENTS_DRUID
from interface.item_set_link import ItemSetLink
from interface import SpellLink
from common.format import format_percentage

CONSUME_BUFFER_MS = 50

WINNING_STREAK_BOOST_PER_STACK = 0.03
WINNING_STREAK_BUFFED_SPELLS = [
  SPELLS.FEROCIOUS_BITE,
  SPELLS.RAVAGE_DOTC_CAT,
  TALENTS_DRUID.PRIMAL_WRATH_TALENT,
  SPELLS.RIP,
  SPELLS.RAMPANT_FEROCITY,
]

BIG_WINNER_DOT_BOOST = 0.16
BIG_WINNER_BUFFED_SPELLS = [
  SPELLS.THRASH_FERAL,
  SPELLS.THRASH_FERAL_BLEED,
  SPELLS.RIP,
  SPELLS.RAKE,
  SPELLS.RAKE_BLEED,
  TALENTS_DRUID.FERAL_FRENZY_TALENT,
  SPELLS.ADAPTIVE_SWARM_DAMAGE,
  SPELLS.BLOODSEEKER_VINES,
  SPELLS.DREADFUL_WOUND,
]

class TWW2TierSet(Analyzer):
  def __init__(self, options: Options):
    super().__init__(options)
    self.has4pc = self.selected_combatant.has4_piece_by_tier(TIERS.TWW2)
    self.active = self.selected_combatant.has2_piece_by_tier(TIERS.TWW2)

    self.winning_streak_buff_damage = 0
    self.big_winner_direct_damage = 0
    self.big_winner_buff_damage = 0

    self.total_base_winning_streak_damage_times_stacks = 0
    self.total_base_winning_streak_damage = 0

    self.add_event_listener(
      Events.damage.by(SELECTED_PLAYER).spell(WINNING_STREAK_BUFFED_SPELLS),
      self.on_winning_streak_buffed_damage,
    )
    if self.has4pc:
      self.add_event_listener(
        Events.damage.by(SELECTED_PLAYER).spell(SPELLS.FERAL_DRUID_BIG_WINNER),
        self.on_big_winner_direct_damage,
      )
      self.add_event_listener(
        Events.damage.by(SELECTED_PLAYER).spell(BIG_WINNER_BUFFED_SPELLS),
        self.on_big_winner_buffed_damage,
      )

  def on_winning_streak_buffed_damage(self, event: DamageEvent):
    stacks = self.selected_combatant.get_buff_stacks(
      SPELLS.FERAL_DRUID_WINNING_STREAK,
      None,
      CONSUME_BUFFER_MS,
    )
    boost = stacks * WINNING_STREAK_BOOST_PER_STACK
    self.winning_streak_buff_damage += calculate_effective_damage(event, boost)

    base_damage = effective_damage(event) / (1 + boost)
    self.total_base_winning_streak_damage += base_damage
    self.total_base_winning_streak_damage_times_stacks += base_damage * stacks

  def on_big_winner_direct_damage(self, event: DamageEvent):
    self.big_winner_direct_damage += effective_damage(event)

  def on_big_winner_buffed_damage(self, event: DamageEvent):
    if self.selected_combatant.has_buff(SPELLS.FERAL_DRUID_BIG_WINNER):
      self.big_winner_buff_damage += calculate_effective_damage(event, BIG_WINNER_DOT_BOOST)

  @property
  def total_2pc_damage(self):
    return self.winning_streak_buff_damage

  @property
  def total_4pc_damage(self):
    return self.big_winner_direct_damage + self.big_winner_buff_damage

  @property
  def avg_stacks(self):
    if self.total_base_winning_streak_damage == 0:
      return 'N/A'
    return f"{self.total_base_winning_streak_damage_times_stacks / self.total_base_winning_streak_damage:.1f}"
