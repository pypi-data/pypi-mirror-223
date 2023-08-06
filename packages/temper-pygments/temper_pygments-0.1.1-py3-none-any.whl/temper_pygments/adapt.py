import pygments.unistring as uni
from pygments.lexer import Lexer, bygroups, include, inherit, using
from pygments.token import Token
from temper_syntax.pygments import ByGroups, Kind, Include, Inherit, Rule, Using


def adapt_kind(kind):
    if isinstance(kind, ByGroups):
        return bygroups(*[adapt_kind(sub) for sub in kind.kinds])
    elif isinstance(kind, Kind):
        return kinds[kind.name]
    elif isinstance(kind, Using):
        return using(lexers[kind.lexer])
    raise ValueError(f"unknown kind: {kind}")


def adapt_regex(regex: str):
    return regex.replace("<<Lu>>", uni.Lu).replace("<<Ll>>", uni.Ll)


def adapt_rule(rule):
    if isinstance(rule, Include):
        return include(rule.state)
    elif isinstance(rule, Inherit):
        return inherit
    elif isinstance(rule, Rule):
        result = (adapt_regex(rule.regex), adapt_kind(rule.kind))
        if rule.state is not None:
            result = (*result, rule.state)
        return result
    raise ValueError(f"unknown rule type: {rule}")


def adapt_rules(rules):
    return [adapt_rule(rule) for rule in rules]


def adapt_tokens(tokens):
    return {key: adapt_rules(rules) for key, rules in tokens.items()}


kinds = {
    "Comment.Multiline": Token.Comment.Multiline,
    "Comment.Singleline": Token.Comment.Singleline,
    "Keyword": Token.Keyword,
    "Keyword.Constant": Token.Keyword.Constant,
    "Keyword.Declaration": Token.Keyword.Declaration,
    "Name": Token.Name,
    "Name.Builtin": Token.Name.Builtin,
    "Name.Decorator": Token.Name.Decorator,
    "Number": Token.Number,
    "Operator": Token.Operator,
    "Punctuation": Token.Punctuation,
    "String": Token.String,
    "String.Interpol": Token.String.Interpol,
    "Whitespace": Token.Whitespace,
}

lexers: dict[str, Lexer] = {}
