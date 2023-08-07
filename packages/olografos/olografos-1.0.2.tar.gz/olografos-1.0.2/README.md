# Ολογράφως

Μετατροπή αριθμών (συμπεριλαμβανομέων και δεκαδικών) σε μορφή ολογράφως, με δυνατότητα επιλογής γένους και κλίσης. Παρέχεται και η δυνατότητα για μετατροπή ποσών ευρώ σε μορφή ολογράφως.

Converts Numbers (including decimal points) into words. It also converts the numbers into words for currency.

## Εγκατάσταση

```python
pip install olografos
```

## Χρήση

Εισαγωγή

```python
from olografos import olografos

print(olografos(123456789))
# Output: εκατόν εικοσιτρία εκατομμύρια τετρακόσιες πενηνταέξι χιλιάδες επτακόσια ογδονταεννέα
```

Επιλογές

```python
lexis = olografos(
  123,
 {
  "currency": False
  "klisi": 'onomastiki'
  "genos": 'oudetero'
 }
)
```

```python
let lexis = olografos(123)
// lexis = εκατόν είκοσι τρία

lexis = olografos(123.45)
// lexis = εκατόν είκοσι τρία και σαράντα πέντε εκατοστά
```

Για μετατροπή σε ευρώ

```python
money = olografos(452, { "currency": True })
// money = τετρακόσια πενήντα δύο ευρώ

money = olografos(452.36, { "currency": True })
// money = τετρακόσια πενήντα δύο ευρώ και τριάντα έξι λεπτά
```

Αλλαγή γένου και κλίσης

```python
lexis = olografos(452, { "klisi": "aitiatiki", "genos": "thyliko" })
// lexis = τετρακοσίες πενήντα δύο
```

Εκατοστά

```python
lexis = olografos(1.57, { "klisi": "geniki" });
// lexis = ενός και πενηνταεπτά εκατοστών
```

## Options

| Επιλογή  | Type                                      | Default      | Descr,{options}iption                         |
| -------- | ----------------------------------------- | ------------ | --------------------------------------------- |
| currency | boolean                                   | False        | Μετατροπή του αριθμόυ σε μορφή ολογράφως ευρώ |
| klisi    | 'onomastiki'<br/>'geniki'<br/>'aitiatiki' | 'onomastiki' | Η κλίση στην οποία θα γραφεί ο αριθμός        |
| genos    | 'arseniko'<br/>'thyliko'<br/>'oudetero'   | 'oudetero'   | Το γένος στο οποίο θα γραφεί ο αριθμός        |
