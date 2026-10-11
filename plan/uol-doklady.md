# UOL API: doklady z účetního systému (zjištěno 2026-10-11)

Zdroj: https://api.uol.cz/openapi.yaml (UOL Accounting REST API 1.0.5). Auth: Basic (e-mail uživatele : API token), uživatel musí mít oprávnění „REST API“. Produkční server `https://{customerId}.ucetnictvi.uol.cz/api` (customerId = subdoména Ondřejova UOL, **zatím neznám**), demo `https://test.demo.uol.cz/api`. Limit 30 požadavků / 10 s. Klíč ve scratchpadu `.uol_basic`, do repa ne; do Vercelu jen přes konektor (sensitive).

Co API umí (to, co potřebujeme): `POST /v1/contacts` (kupující), `POST /v1/sales_invoices` (faktura; `status: confirmed` = vystavená, `external_id` = naše ID objednávky pro idempotenci, `variable_symbol`, `payment_method`, `send_by_email`), `GET /v1/sales_invoices/{id}` s `Accept: application/pdf` (PDF) nebo `text/isdoc`. Číslo dokladu přiděluje UOL (`public_id`). Potvrzenou fakturu nejde smazat ani upravit bez `repairs`.

Otevřené (účetní): 1) neplátce DPH: faktura, nebo příjmový doklad / jiný typ; 2) jak označit zaplaceno (párování s Fio importem v UOL, Stripe platba se na účet dostane až výplatou); 3) zda UOL sám pošle PDF kupujícímu (`send_by_email`), nebo ho přiloží naše aplikace.

Návrh napojení (až po odpovědi účetní): po `markPaid` aplikace vytvoří kontakt + potvrzenou fakturu s `external_id`, stáhne PDF a přiloží ho k doručovacímu e-mailu místo našeho `/doklad`; při výpadku UOL se doručení NEZASTAVÍ (záložní vlastní doklad, opakování na pozadí). Dokud se neví, doklady se nemění.
