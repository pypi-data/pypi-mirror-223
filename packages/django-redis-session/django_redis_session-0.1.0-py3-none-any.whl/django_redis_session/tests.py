import time
from django.test import TestCase

from django_redis_session.session_store import SessionStore


class RedisSessionTestCase(TestCase):
    def setUp(self) -> None:
        self.redis_session = SessionStore()

    def test_modify_and_keys(self):
        self.assertFalse(self.redis_session.modified)

        self.redis_session["test_key"] = "test_value"
        self.assertTrue(self.redis_session.modified)
        self.assertEqual(self.redis_session["test_key"], "test_value")

    def test_save_and_delete(self):
        self.redis_session["key"] = "value"
        self.redis_session.save()

        self.assertTrue(self.redis_session.exists(self.redis_session.session_key))

        self.redis_session.delete(self.redis_session.session_key)
        self.assertFalse(self.redis_session.exists(self.redis_session.session_key))

    def test_flush(self):
        self.redis_session["key"] = "another_value"
        self.redis_session.save()
        key = self.redis_session.session_key
        self.redis_session.flush()
        self.assertFalse(self.redis_session.exists(key))

    def test_items(self):
        self.redis_session["item1"], self.redis_session["item2"] = 1, 2
        self.redis_session.save()

        self.assertEqual(
            set(list(self.redis_session.items())), {("item2", 2), ("item1", 1)}
        )

    def test_expiry(self):
        self.redis_session.set_expiry(1)
        self.assertEqual(self.redis_session.get_expiry_age(), 1)

        self.redis_session["key"] = "expiring_value"
        self.redis_session.save()
        key = self.redis_session.session_key
        self.assertTrue(self.redis_session.exists(key))

        time.sleep(2)
        self.assertFalse(self.redis_session.exists(key))
