from odoo.tests.common import TransactionCase


class TestTaskCheckList(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.checklist1 = cls.env["task.checklist"].create({"name": "Step 1"})
        cls.checklist2 = cls.env["task.checklist"].create({"name": "Step 2"})
        cls.project = cls.env["project.project"].create({"name": "Test Project"})
        cls.task = cls.env["project.task"].create(
            {"name": "Test Task", "project_id": cls.project.id}
        )

    def test_progress_zero_no_items_selected(self):
        self.task.task_checklist = [(5,)]
        self.task._compute_checklist_progress()
        self.assertEqual(self.task.checklist_progress, 0.0)

    def test_progress_partial(self):
        self.task.task_checklist = [(6, 0, [self.checklist1.id])]
        self.task._compute_checklist_progress()
        total = self.env["task.checklist"].search_count([])
        expected = 1 * 100.0 / total
        self.assertAlmostEqual(self.task.checklist_progress, expected)

    def test_progress_full(self):
        self.task.task_checklist = [(6, 0, [self.checklist1.id, self.checklist2.id])]
        self.task._compute_checklist_progress()
        total = self.env["task.checklist"].search_count([])
        expected = 2 * 100.0 / total
        self.assertAlmostEqual(self.task.checklist_progress, expected)
