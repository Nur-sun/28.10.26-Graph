import unittest
from graph import CityGraph
from dijkstra import dijkstra

class DijkstraTests(unittest.TestCase):
    def setUp(self):
        self.g = CityGraph()

    def test_A_to_O_distance(self):
        result = dijkstra(self.g, "A", "O", "distance")
        self.assertEqual(result["total"], 21)
        self.assertEqual(result["route"], ["A","C","F","E","H","I","L","M","O"])

    def test_same_node(self):
        result = dijkstra(self.g, "A", "A")
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["route"], ["A"])

    def test_missing_node(self):
        with self.assertRaises(ValueError):
            dijkstra(self.g, "A", "Z")

    def test_negative_weight_rejected(self):
        with self.assertRaises(ValueError):
            self.g.add_edge("A","B",-1,2)

    def test_zero_weight(self):
        self.g.add_edge("A","O",0,0)
        result = dijkstra(self.g,"A","O")
        self.assertEqual(result["total"],0)

    def test_closed_edge_recalculates(self):
        original = dijkstra(self.g,"A","O")["total"]
        self.g.toggle_edge("A","C",True)
        updated = dijkstra(self.g,"A","O")["total"]
        self.assertGreater(updated, original)

    def test_isolated_node(self):
        self.g.add_node("P")
        result = dijkstra(self.g,"A","P")
        self.assertIsNone(result["total"])
        self.assertEqual(result["route"], [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
