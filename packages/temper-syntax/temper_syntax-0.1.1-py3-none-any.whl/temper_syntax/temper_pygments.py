from temper_core import TemperObject as TemperObject0, cast_by_type as cast_by_type5, Pair as Pair_255, map_constructor as map_constructor_256, list_join as list_join_257, str_cat as str_cat_258
from typing import Tuple as Tuple3, Any as Any1, Callable as Callable6
from builtins import tuple as tuple4
from temper_syntax.pygments import RuleOption as RuleOption__8, Rule as Rule__9, Include as Include__10, whitespace as Whitespace__33, Kind as Kind__14, comment_singleline as CommentSingleline__21, comment_multiline as CommentMultiline__20, keyword_constant as KeywordConstant__23, keyword_declaration as KeywordDeclaration__24, keyword as Keyword__22, name_builtin as NameBuiltin__26, string_kind as StringKind__31, operator as Operator__29, punctuation as Punctuation__30, number as Number__28, name_decorator as NameDecorator__27, name as Name__25, string_interpol as StringInterpol__32, include as include__11, Inherit as Inherit__12, TokenKind as TokenKind__13, ByGroups as ByGroups__15, bygroups as bygroups__16, Using as Using__17, using as using__18, inherit as inherit__19
class TemperLexer(TemperObject0):
  name__34: 'str'
  aliases__35: 'Tuple3[str, ...]'
  filenames__36: 'Tuple3[str, ...]'
  tokens__37: 'Map__16[str, (Tuple3[RuleOption__8, ...])]'
  __slots__ = ('name__34', 'aliases__35', 'filenames__36', 'tokens__37')
  def constructor__38(this__0, name: 'str' = ..., aliases: 'Tuple3[str, ...]' = ..., filenames: 'Tuple3[str, ...]' = ..., tokens: 'Map__16[str, (Tuple3[RuleOption__8, ...])]' = ...) -> Any1:
    name__39: 'str' = name
    aliases__40: 'Tuple3[str, ...]' = aliases
    filenames__41: 'Tuple3[str, ...]' = filenames
    tokens__42: 'Map__16[str, (Tuple3[RuleOption__8, ...])]' = tokens
    return__4: 'None'
    t_207: 'Rule__9'
    t_209: 'Rule__9'
    t_210: 'Rule__9'
    t_211: 'Rule__9'
    t_212: 'Map__16[str, (Tuple3[RuleOption__8, ...])]'
    t_213: 'Pair__22[str, (Tuple3[RuleOption__8, ...])]'
    t_214: 'Rule__9'
    t_215: 'Rule__9'
    t_216: 'Pair__22[str, (Tuple3[RuleOption__8, ...])]'
    t_217: 'Include__10'
    t_218: 'Pair__22[str, (Tuple3[RuleOption__8, ...])]'
    t_219: 'Rule__9'
    t_220: 'Rule__9'
    t_221: 'Rule__9'
    t_222: 'Pair__22[str, (Tuple3[RuleOption__8, ...])]'
    t_223: 'Rule__9'
    t_224: 'Rule__9'
    t_225: 'str'
    t_226: 'str'
    t_227: 'str'
    t_228: 'str'
    t_229: 'Rule__9'
    t_230: 'Rule__9'
    t_231: 'Rule__9'
    t_232: 'Rule__9'
    t_233: 'Rule__9'
    t_234: 'Rule__9'
    t_235: 'Rule__9'
    t_236: 'Rule__9'
    t_237: 'Rule__9'
    t_238: 'Rule__9'
    t_133: 'Tuple3[RuleOption__8, ...]'
    t_139: 'Tuple3[RuleOption__8, ...]'
    t_143: 'Tuple3[RuleOption__8, ...]'
    t_148: 'Tuple3[RuleOption__8, ...]'
    if name__39 is ...:
      name__39 = 'Temper'
    if aliases__40 is ...:
      aliases__40 = ('temper',)
    if filenames__41 is ...:
      filenames__41 = ('*.temper',)
    if tokens__42 is ...:
      t_207 = Rule__9('\\s+', Whitespace__33)
      t_223 = Rule__9('//.*?$', CommentSingleline__21)
      t_224 = Rule__9('/\\*', CommentMultiline__20, 'nestedcomment')
      t_225 = words__6('false', 'NaN', 'null', 'true', 'void')
      t_238 = Rule__9(t_225, KeywordConstant__23)
      t_226 = words__6('class', 'interface', 'let', 'private', 'public', 'sealed', 'var')
      t_237 = Rule__9(t_226, KeywordDeclaration__24)
      t_227 = words__6('do', 'else', 'export', 'extends', 'fn', 'if', 'import', 'is', 'match', 'new', 'orelse')
      t_236 = Rule__9(t_227, Keyword__22)
      t_228 = words__6('AnyValue', 'Boolean', 'Float64', 'Function', 'Int', 'List', 'ListBuilder', 'Listed', 'Map', 'MapBuilder', 'MapKey', 'Mapped', 'NoResult', 'Null', 'String', 'StringSlice', 'Void')
      t_235 = Rule__9(t_228, NameBuiltin__26)
      t_229 = Rule__9('"', StringKind__31, 'string')
      t_230 = Rule__9('[-=+*&|<>]+|/=?', Operator__29)
      t_231 = Rule__9('[{}();:.,]', Punctuation__30)
      t_232 = Rule__9('\\d+\\.?\\d*|\\.\\d+', Number__28)
      t_233 = Rule__9('@[_<<Lu>><<Ll>>][_<<Lu>><<Ll>>0-9]*', NameDecorator__27)
      t_234 = Rule__9('[_<<Lu>><<Ll>>][_<<Lu>><<Ll>>0-9]*', Name__25)
      t_133 = cast_by_type5((t_207, t_223, t_224, t_238, t_237, t_236, t_235, t_229, t_230, t_231, t_232, t_233, t_234), tuple4)
      t_222 = Pair_255('root', t_133)
      t_209 = Rule__9('[^*/]+', CommentMultiline__20)
      t_219 = Rule__9('/\\*', CommentMultiline__20, '#push')
      t_220 = Rule__9('\\*/', CommentMultiline__20, '#pop')
      t_221 = Rule__9('[*/]', CommentMultiline__20)
      t_139 = cast_by_type5((t_209, t_219, t_220, t_221), tuple4)
      t_218 = Pair_255('nestedcomment', t_139)
      t_210 = Rule__9('}', StringInterpol__32, '#pop')
      t_217 = include__11('root')
      t_143 = cast_by_type5((t_210, t_217), tuple4)
      t_216 = Pair_255('interpolation', t_143)
      t_211 = Rule__9('"', StringKind__31, '#pop')
      t_214 = Rule__9('\\$\\{', StringInterpol__32, 'interpolation')
      t_215 = Rule__9('(?:[^"$]|\\$[^{])+', StringKind__31)
      t_148 = cast_by_type5((t_211, t_214, t_215), tuple4)
      t_213 = Pair_255('string', t_148)
      t_212 = map_constructor_256((t_222, t_218, t_216, t_213))
      tokens__42 = t_212
    this__0.name__34 = name__39
    this__0.aliases__35 = aliases__40
    this__0.filenames__36 = filenames__41
    this__0.tokens__37 = tokens__42
    return__4 = None
    return return__4
  def __init__(this__0, name: 'str' = ..., aliases: 'Tuple3[str, ...]' = ..., filenames: 'Tuple3[str, ...]' = ..., tokens: 'Map__16[str, (Tuple3[RuleOption__8, ...])]' = ...) -> None:
    name__39: 'str' = name
    aliases__40: 'Tuple3[str, ...]' = aliases
    filenames__41: 'Tuple3[str, ...]' = filenames
    tokens__42: 'Map__16[str, (Tuple3[RuleOption__8, ...])]' = tokens
    this__0.constructor__38(name__39, aliases__40, filenames__41, tokens__42)
  @property
  def name(this__48) -> 'str':
    return__49: 'str'
    return__49 = this__48.name__34
    return return__49
  @property
  def aliases(this__52) -> 'Tuple3[str, ...]':
    return__53: 'Tuple3[str, ...]'
    return__53 = this__52.aliases__35
    return return__53
  @property
  def filenames(this__56) -> 'Tuple3[str, ...]':
    return__57: 'Tuple3[str, ...]'
    return__57 = this__56.filenames__36
    return return__57
  @property
  def tokens(this__60) -> 'Map__16[str, (Tuple3[RuleOption__8, ...])]':
    return__61: 'Map__16[str, (Tuple3[RuleOption__8, ...])]'
    return__61 = this__60.tokens__37
    return return__61
def words__6(*names__43: 'str') -> 'str':
  global list_join_257, str_cat_258
  return__5: 'str'
  def fn__240(x__45: 'str') -> 'str':
    return__155: 'str'
    return__155 = x__45
    return return__155
  t_242: 'Callable6[[str], str]' = fn__240
  t_243: 'str' = list_join_257(names__43, '|', t_242)
  return__5 = str_cat_258('\\b(?:', t_243, ')\\b')
  return return__5
nameRegex__7: 'str' = '[_<<Lu>><<Ll>>][_<<Lu>><<Ll>>0-9]*'
return__154: 'None' = None
export = return__154
