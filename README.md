# SenRiver

## Wstęp
Repozytorium zawiera skrypty pozwalające na automatyczne wygenerowanie datasetu zawierającego zdjęcia satelitarne rzek oraz odpowiadające im maski wskazujące piksele zawierające wodę na podstawie geoprzestrzennych danych zawierających informacje o współrzędnych geograficznych największych rzek świata i bazy znormalizowanych zdjęć satelitarnych z bazy Sentinel-2 Global Mosaic.

## Opis działania
1) Pobranie informacji o współrzędnych geograficznych i kształcie danej rzeki z bazy utworzonej w ramach publikacji [1](https://doi.org/10.1038/s41597-019-0243-y)
2) Utworzenie wokół kształtu rzeki siatki nienakładających się kwadratów.
3) Pobranie wielkopowierzchniowych plików rastrowych z bazy Sentinel-2 Global Mosaic.
4) podział plików pobranych w punkcie 3) na małe cześci zdefiniowane przez siatkę wygenerowaną w punkcie 2).
5) progowanie obrazów z pasma podczerwieni w celu uzyskania masek cieków oraz zbiorników wodnych.

## Dataset
Dotychczasowo wygenerowany dataset można pobrać na stronie https://mega.nz/folder/jOBTGYzb#PjvUwnPX6fcFdEzllDu_tg. Zawiera on ponad 3300 par kolorowych zdjęć oraz odpowiadających im masek dla następujących rzek:
- Amazonka,
- Kongo,
- Dunaj,
- Lualaba,
- Madeira,
- Missisipi,
- Orinoco.

## Odniesienia

[1] Yan, D., Wang, K., Qin, T. et al. A data set of global river networks and corresponding water resources zones divisions. Sci Data 6, 219 (2019). https://doi.org/10.1038/s41597-019-0243-y
