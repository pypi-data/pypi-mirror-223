from temper_core import TemperObject as TemperObject0
from typing import Any as Any1, Union as Union2, Tuple as Tuple3
class RuleOption(TemperObject0):
  __slots__ = ()
  def constructor__19(this__0) -> Any1:
    return__1: 'None'
    return__1 = None
    return return__1
  def __init__(this__0) -> None:
    this__0.constructor__19()
class Rule(RuleOption):
  regex__20: 'str'
  kind__21: 'TokenKind'
  state__22: 'Union2[str, None]'
  __slots__ = ('regex__20', 'kind__21', 'state__22')
  def constructor__23(this__2, regex__24: 'str', kind__25: 'TokenKind', state: 'Union2[str, None]' = ...) -> Any1:
    state__26: 'Union2[str, None]' = state
    return__4: 'None'
    if state__26 is ...:
      state__26 = None
    this__2.regex__20 = regex__24
    this__2.kind__21 = kind__25
    this__2.state__22 = state__26
    return__4 = None
    return return__4
  def __init__(this__2, regex__24: 'str', kind__25: 'TokenKind', state: 'Union2[str, None]' = ...) -> None:
    state__26: 'Union2[str, None]' = state
    this__2.constructor__23(regex__24, kind__25, state__26)
  @property
  def regex(this__48) -> 'str':
    return__49: 'str'
    return__49 = this__48.regex__20
    return return__49
  @property
  def kind(this__52) -> 'TokenKind':
    return__53: 'TokenKind'
    return__53 = this__52.kind__21
    return return__53
  @property
  def state(this__56) -> 'Union2[str, None]':
    return__57: 'Union2[str, None]'
    return__57 = this__56.state__22
    return return__57
class Include(RuleOption):
  state__27: 'str'
  __slots__ = ('state__27',)
  def constructor__28(this__5, state__29: 'str') -> Any1:
    return__6: 'None'
    this__5.state__27 = state__29
    return__6 = None
    return return__6
  def __init__(this__5, state__29: 'str') -> None:
    this__5.constructor__28(state__29)
  @property
  def state(this__60) -> 'str':
    return__61: 'str'
    return__61 = this__60.state__27
    return return__61
class Inherit(Rule):
  __slots__ = ()
  def constructor__32(this__8) -> Any1:
    return__9: 'None'
    return__9 = None
    return return__9
  def __init__(this__8) -> None:
    this__8.constructor__32()
class TokenKind(TemperObject0):
  __slots__ = ()
class Kind(TokenKind):
  name__33: 'str'
  __slots__ = ('name__33',)
  def constructor__34(this__10, name__35: 'str') -> Any1:
    return__11: 'None'
    this__10.name__33 = name__35
    return__11 = None
    return return__11
  def __init__(this__10, name__35: 'str') -> None:
    this__10.constructor__34(name__35)
  @property
  def name(this__63) -> 'str':
    return__64: 'str'
    return__64 = this__63.name__33
    return return__64
class ByGroups(TokenKind):
  kinds__36: 'Tuple3[TokenKind, ...]'
  __slots__ = ('kinds__36',)
  def constructor__37(this__12, kinds__38: 'Tuple3[TokenKind, ...]') -> Any1:
    return__14: 'None'
    this__12.kinds__36 = kinds__38
    return__14 = None
    return return__14
  def __init__(this__12, kinds__38: 'Tuple3[TokenKind, ...]') -> None:
    this__12.constructor__37(kinds__38)
  @property
  def kinds(this__67) -> 'Tuple3[TokenKind, ...]':
    return__68: 'Tuple3[TokenKind, ...]'
    return__68 = this__67.kinds__36
    return return__68
class Using(TokenKind):
  lexer__41: 'str'
  __slots__ = ('lexer__41',)
  def constructor__42(this__16, lexer__43: 'str') -> Any1:
    return__17: 'None'
    this__16.lexer__41 = lexer__43
    return__17 = None
    return return__17
  def __init__(this__16, lexer__43: 'str') -> None:
    this__16.constructor__42(lexer__43)
  @property
  def lexer(this__71) -> 'str':
    return__72: 'str'
    return__72 = this__71.lexer__41
    return return__72
def include(state__30: 'str') -> 'Include':
  return__7: 'Include'
  t_218: 'Include' = Include(state__30)
  return__7 = t_218
  return return__7
t_226: 'Inherit' = Inherit()
inherit: 'Inherit' = t_226
t_227: 'Kind' = Kind('Comment.Multiline')
comment_multiline: 'Kind' = t_227
t_229: 'Kind' = Kind('Comment.Singleline')
comment_singleline: 'Kind' = t_229
t_231: 'Kind' = Kind('Keyword')
keyword: 'Kind' = t_231
t_233: 'Kind' = Kind('Keyword.Constant')
keyword_constant: 'Kind' = t_233
t_235: 'Kind' = Kind('Keyword.Declaration')
keyword_declaration: 'Kind' = t_235
t_237: 'Kind' = Kind('Name')
name: 'Kind' = t_237
t_239: 'Kind' = Kind('Name.Builtin')
name_builtin: 'Kind' = t_239
t_241: 'Kind' = Kind('Name.Decorator')
name_decorator: 'Kind' = t_241
t_243: 'Kind' = Kind('Number')
number: 'Kind' = t_243
t_245: 'Kind' = Kind('Operator')
operator: 'Kind' = t_245
t_247: 'Kind' = Kind('Punctuation')
punctuation: 'Kind' = t_247
t_249: 'Kind' = Kind('String')
string_kind: 'Kind' = t_249
t_251: 'Kind' = Kind('String.Interpol')
string_interpol: 'Kind' = t_251
t_253: 'Kind' = Kind('Whitespace')
whitespace: 'Kind' = t_253
def bygroups(kinds__39: 'Tuple3[TokenKind, ...]') -> 'ByGroups':
  return__15: 'ByGroups'
  t_211: 'ByGroups' = ByGroups(kinds__39)
  return__15 = t_211
  return return__15
def using(lexer__44: 'str') -> 'Using':
  return__18: 'Using'
  t_207: 'Using' = Using(lexer__44)
  return__18 = t_207
  return return__18
return__156: 'None' = None
export = return__156
