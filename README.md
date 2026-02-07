# VA_project
Projekt na VA

##  Základní nápad
Jednalo  by se o jednoduchou 2D platformovou hru v 8-bitovém stylu s pohledem z boku. 
Hráč ovládá postavu a jeho úkolem je projít jednotlivé levely a dostat se do jejich cíle. Během hry bude se bude muset pohybovat kolem, ať už z důvodů parkuru, který by byl potřeba k dokončení levelu ale také kvůli překonáváni různých překážek a vyhýbání se enemákům, po případně s nimi bojovat. Hra bude obsahovat více levelů.
Součástí bude také jednoduchý level editor, který jak usnadní práci mě, tak také dá možnost hráčům vytvářet si své vlastní levely. 

## Formálně
Hra se bude skládat ze smyčky, která bude zpracovávat:
-	Vstupy od hráče
-	Fyziku pohybu
-	Interakce s objekty, a enemáky
-	Vykreslování herní scény
Levely budou reprezentovány datovou strukturou, která bude načítaná hrou ze souborů vytvořených v level editoru.

## Implementace
Aplikace bude implementována v Pythonu.
Herní logika bude oddělena od vykreslování a výstupů. Každý level bude tvořen sadou objektů, které budou mít své vlastní chování, podle toho, jakým objektem jsou.
Level editor bude umožňovat vytváření a ukládání levelů do souborů, které následně bude hra přímo načítat.

## Interface
Hra bude ovládána s pomocí klávesnice.
Uživatel bude mít možnost buď spustit hru a hrát již před vytvořené levely, nebo spustit level editor a vytvářet své vlastní, které pak bude moct samozřejmě i hrát. 
Výstupem bude vykreslená herní scéna a případné informace o stavu postavy hráče, které budou zahrnovat např. životy. 

## Použité knihovny
Základ bude realizován s pomocí standartních knihoven v Pythonu. Následně také externí knihovny typu Pygame pro grafiku a zpracování vstupů. Případné další knihovny budou uvedeny. 
