---
title: Passay Password Policy
impact: MEDIUM
tags: password, policy, validation, passay, security
---

# Passay Password Policy

Dieser Skill beschreibt Passay - Passwort-Policy-Enforcement fuer Validierung und Generierung.

### Maven

```xml
<properties>
    <passay.version>1.6.6</passay.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.passay</groupId>
        <artifactId>passay</artifactId>
        <version>${passay.version}</version>
    </dependency>
</dependencies>
```

---

### Password Validierung

```java
PasswordValidator validator = new PasswordValidator(
    new LengthRule(8, 64),
    new CharacterRule(EnglishCharacterData.UpperCase, 1),
    new CharacterRule(EnglishCharacterData.LowerCase, 1),
    new CharacterRule(EnglishCharacterData.Digit, 1),
    new CharacterRule(EnglishCharacterData.Special, 1),
    new WhitespaceRule()
);

RuleResult result = validator.validate(new PasswordData(password));

if (result.isValid()) {
    // Passwort ok
} else {
    List<String> messages = validator.getMessages(result);
}
```

---

### M von N Regeln

```java
// Mindestens 3 von 4 Zeichenklassen
CharacterCharacteristicsRule charRule = new CharacterCharacteristicsRule();
charRule.setNumberOfCharacteristics(3);
charRule.getRules().add(new CharacterRule(EnglishCharacterData.UpperCase, 1));
charRule.getRules().add(new CharacterRule(EnglishCharacterData.LowerCase, 1));
charRule.getRules().add(new CharacterRule(EnglishCharacterData.Digit, 1));
charRule.getRules().add(new CharacterRule(EnglishCharacterData.Special, 1));
```

---

### Verfügbare Rules

| Rule | Beschreibung |
|------|--------------|
| `LengthRule(min, max)` | Passwortlänge |
| `CharacterRule(data, count)` | Min. Anzahl aus Zeichenklasse |
| `WhitespaceRule` | Keine Leerzeichen |
| `IllegalSequenceRule(data, len)` | Keine Sequenzen (abc, 123) |
| `RepeatCharacterRegexRule(count)` | Keine Wiederholungen (aaa) |

---

### Passwort Generierung

```java
List<CharacterRule> rules = Arrays.asList(
    new CharacterRule(EnglishCharacterData.UpperCase, 2),
    new CharacterRule(EnglishCharacterData.LowerCase, 4),
    new CharacterRule(EnglishCharacterData.Digit, 2),
    new CharacterRule(EnglishCharacterData.Special, 1)
);

PasswordGenerator generator = new PasswordGenerator();
String password = generator.generatePassword(12, rules);
```

---

### Service-Klasse

```java
@Component
public class PasswordPolicyService {
    private final PasswordValidator _validator;
    private final PasswordGenerator _generator;

    public ImmutableList<String> validate(final String password) {
        RuleResult result = _validator.validate(new PasswordData(password));
        if (result.isValid()) {
            return Lists.immutable.empty();
        }
        return Lists.immutable.ofAll(_validator.getMessages(result));
    }

    public String generate(final int length) {
        return _generator.generatePassword(length, rules);
    }
}
```

---

### Best Practices

1. **Keine max-Länge unter 64** - Passwort-Manager unterstützen
2. **M von N statt alle** - 3 von 4 Zeichenklassen
3. **Sequenzen blocken** - qwerty, 12345
4. **Custom Messages** - Deutsche Fehlermeldungen

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt
- [ ] PasswordValidator konfiguriert
- [ ] LengthRule (min 8, max 64+)
- [ ] CharacterRules (3 von 4)
- [ ] Service-Klasse implementiert
- [ ] Fehlermeldungen lokalisiert (optional)
