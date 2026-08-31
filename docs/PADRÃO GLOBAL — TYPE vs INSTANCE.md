# 📘 📐 PADRÃO GLOBAL — TYPE vs INSTANCE

---

# 1. 🎯 PRINCÍPIO FUNDAMENTAL

```text
TYPE  → define o que o elemento DEVE ser (projeto / especificação)
INSTANCE → define o que o elemento É (modelo IFC / realidade)
```

---

# 2. 🧠 REGRA DE OURO

```text
Se o valor é definido antes da existência física → TYPE
Se o valor depende da instância/modelo → INSTANCE
```

---

# 3. 🏗️ ESTRUTURA PADRÃO NA ONTOLOGIA

## 🔹 TYPE (engenharia)

```ttl
Element
    edo:hasAttribute → Attribute (TypeLevel)
    edo:hasSpec → Spec
        Spec → hasAttribute → Attribute (TypeLevel)
```

---

## 🔹 INSTANCE (IFC / modelo)

```text
IfcElement (instância)
    → Pset_Element
        → atributos InstanceLevel

IfcMaterial
    → Pset_Material
        → atributos InstanceLevel
```

---

# 4. 🧩 PADRÃO DE NOMENCLATURA

## 🔹 TYPE → nome base (sem sufixo)

```text
Material
Length
Pressure
Temperature
CorrosionAllowance
```

---

## 🔹 INSTANCE → nome qualificado (OBRIGATÓRIO)

### 🏆 Padrão principal:

```text
AppliedX
ActualX
MeasuredX
```

---

# 5. 📚 DICIONÁRIO DE PREFIXOS (OFICIAL)

Use sempre um desses — isso padroniza toda ontologia:

| Prefixo       | Quando usar                          | Exemplo            |
| ------------- | ------------------------------------ | ------------------ |
| **Applied**   | algo atribuído no modelo IFC         | `AppliedMaterial`  |
| **Actual**    | valor real (pode diferir do projeto) | `ActualLength`     |
| **Measured**  | valor medido                         | `MeasuredPressure` |
| **Installed** | estado após instalação               | `InstalledDepth`   |
| **AsBuilt**   | conforme construído                  | `AsBuiltThickness` |

---

# 6. 🚫 REGRAS DE OURO (OBRIGATÓRIAS)

## ❌ Nunca fazer

```text
Mesmo nome com scopes diferentes
```

❌ ERRADO:

```ttl
Material (Type)
Material (Instance)
```

---

## ❌ Nunca inferir pelo contexto

```text
"Está em IfcMaterial então é instance"
```

👉 O nome TEM que deixar explícito

---

## ❌ Nunca usar nomes genéricos

```text
Value
Data
Info
Property
```

---

# 7. ✅ PADRÃO DE MODELAGEM

## 🔹 TYPE

```ttl
edo:Material
    edo:hasAttributeScope edo:TypeLevelAttribute .
```

---

## 🔹 INSTANCE

```ttl
edo:AppliedMaterial
    edo:hasAttributeScope edo:InstanceLevelAttribute .
```

---

# 8. 🔁 MAPEAMENTO TYPE → INSTANCE

| TYPE               | INSTANCE                  |
| ------------------ | ------------------------- |
| Material           | AppliedMaterial           |
| Length             | ActualLength              |
| Pressure           | MeasuredPressure          |
| Temperature        | MeasuredTemperature       |
| CorrosionAllowance | AsBuiltCorrosionAllowance |

---

# 9. 🧱 RELAÇÃO COM IFC

## 🔹 TYPE

```text
IfcTypeObject / definição conceitual
```

---

## 🔹 INSTANCE

```text
IfcElement → Pset
IfcMaterial → Pset
```

---

# 10. 🧩 CASOS ESPECIAIS (IMPORTANTES)

## 🔹 Material

| Contexto | Nome            |
| -------- | --------------- |
| Projeto  | Material        |
| IFC      | AppliedMaterial |

---

## 🔹 Dimensões

| Contexto | Nome         |
| -------- | ------------ |
| Projeto  | Length       |
| IFC      | ActualLength |

---

## 🔹 Fluido

| Contexto       | Nome              |
| -------------- | ----------------- |
| Caracterização | Fluid.xxx         |
| Medido         | MeasuredFluid.xxx |

---

# 11. 🧠 REGRA PARA SPECS

```text
Specs → SEMPRE TYPE
```

EXCETO:

👉 quando você explicitamente materializa no IFC (caso raro e controlado)

---

# 12. 🚀 BENEFÍCIOS DO PADRÃO

✔ elimina ambiguidade
✔ simplifica SPARQL
✔ facilita geração de Excel
✔ garante consistência IFC
✔ escala para novos domínios

---

# 13. 📏 CHECKLIST (USO PRÁTICO)

Antes de criar um atributo, valide:

```text
1. Isso é definido em projeto?
   → TYPE

2. Isso existe na instância IFC?
   → INSTANCE

3. O nome deixa isso explícito?
   → se não, corrigir
```

---

# 14. 🧠 EXEMPLO COMPLETO

```ttl
# TYPE
edo:Pipeline
    edo:hasAttribute edo:Material ;
    edo:hasAttribute edo:Length .

# INSTANCE
edo:AppliedMaterial
    edo:hasAttributeScope edo:InstanceLevelAttribute .

edo:ActualLength
    edo:hasAttributeScope edo:InstanceLevelAttribute .
```

---

# ✅ CONCLUSÃO

O padrão global que você deve adotar é:

```text
TYPE      → nome simples (Material, Length, Pressure)
INSTANCE  → nome qualificado (AppliedX, ActualX, MeasuredX)
```

E a regra mais importante:

> **Nunca reutilizar o mesmo nome para TYPE e INSTANCE**

---

Se quiser, posso dar o próximo passo e:

✅ revisar sua ontologia inteira
✅ sugerir renomeação automática
✅ criar regras para seu gerador de Excel/IFC

Isso deixaria seu ecossistema totalmente consistente.
