Optymalizacja przesyłu w sieci światłowodowej przy użyciu algorytmu ewolucyjnego
------

# Treść zadania
Dana jest sieć, opisana za pomocą grafu G=(N,E), gdzie N jest zbiorem węzłów, a E jest zbiorem krawędzi. D jest zbiorem zapotrzebowań, wyrażonych w jednostkach 1Gb/s. Dla każdego zapotrzebowania istnieją co najmniej 3 predefiniowane ścieżki. Każde zapotrzebowanie realizowane jest za pomocą kart transponderów o pojemności 10, 40 i 100G (lambdy). Stworzyć program, który za pomocą algorytmu ewolucyjnego, realizuje wszystkie zapotrzebowania, nie przekraczając pojemność włókna światłowodowego. W jednym włóknie mogą się mieścić 8, 32, 64 i 92 długości fali (lambdy).