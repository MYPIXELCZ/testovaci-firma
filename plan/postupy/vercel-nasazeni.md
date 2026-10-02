# Nasazení webu na Vercel (jen tým MYPIXELCZ)

Pravidlo (Ondřej 2026-10-02 14:17): web se nasazuje výhradně do plánu Pro týmu **MYPIXELCZ**, nikdy do jiného týmu (např. JOYMARK).

Identifikátory: tým `mypixelcz`, `team_fNHd0fCTFAA6MuEnT4BlEeWu`, GitHub organizace MYPIXELCZ. Stav ověřen 2026-10-02: konektor vidí jediný tým (MYPIXELCZ), projekty `printopia` (prj_2qqb7t2Wi8muOarlj04j6vK8lQOP) a `anoberu` (prj_03AAVPn5Unj5aZgXeVvZ3VkGYdes) mají `accountId` = tento tým.

## Kontrolní seznam před i po nasazení
- [ ] `list_teams` obsahuje MYPIXELCZ a je to cílový tým (jiný tým se nepoužije, ani když ho konektor ukáže).
- [ ] Každé volání, které zakládá nebo mění (create_project, create_git_project, create_deployment, add_project_domain, create_project_env, issue_cert, update_project…), má `teamId=team_fNHd0fCTFAA6MuEnT4BlEeWu`.
- [ ] Po založení projektu `get_project`: `accountId` = `team_fNHd0fCTFAA6MuEnT4BlEeWu`, jinak okamžitě STOP, nic dalšího nenasazovat a nahlásit Ondřejovi.
- [ ] Nasazení běží přes push na větev (GitHub MYPIXELCZ → projekt v týmu MYPIXELCZ), ne ručním nahráváním do jiného účtu.
- [ ] Doména se přidává do projektu v týmu MYPIXELCZ (NS ns1/ns2.vercel-dns.com), ne do jiného účtu.
- [ ] Plán projektu `plan/<projekt>.md` má řádek „Vercel tým: MYPIXELCZ (team_fNHd0fCTFAA6MuEnT4BlEeWu)“ s datem ověření.

Hosting webů pro klienty (služba „Web za 24 hodin“) je samostatná otázka, viz `plan/postupy/web-za-24-hodin.md` (Vercel Terms čl. 11); i tam platí, že firma nasazuje jen do plánu MYPIXELCZ.
