import unittest
from event_delegate import Event, InvalidHandlerError


class TestEventLibrary(unittest.TestCase):
    def test_returns(self):
        event = Event()
        self.assertTrue(event.returns == {})

    def test_add_handler(self):
        event = Event()
        def dummy_handler(): pass
        event.add_handler(dummy_handler)
        self.assertTrue(dummy_handler in event._Event__handlers)

    def test_add_handler_exception(self):
        event = Event()
        with self.assertRaises(InvalidHandlerError):
            event.add_handler(None)

    def test_has_handler(self):
        event = Event()
        def dummy_handler(): pass
        event._Event__handlers.append(dummy_handler)
        self.assertTrue(event.has_handler(dummy_handler))

    def test_remove_handler(self):
        event = Event()
        def dummy_handler(): pass
        event._Event__handlers.append(dummy_handler)
        event.remove_handler(dummy_handler)
        self.assertFalse(dummy_handler in event._Event__handlers)

    def test_get_return(self):
        event = Event()
        event._Event__returns = {sum: 0}
        self.assertTrue(event.get_return(sum) == 0)

    def test_get_returns(self):
        event = Event()
        sample = {sum: 0, all: False}
        event._Event__returns = sample
        self.assertTrue(event.get_returns((sum, all)) == sample)

    def test_invoke(self):
        event = Event()
        output = []
        def handler_a(arg): output.append(f'handler_a: {arg}')
        def handler_b(arg): output.append(f'handler_b: {arg}')
        event._Event__handlers = [handler_a, handler_b]
        event.invoke("test")
        expected_output = ['handler_a: test', 'handler_b: test']
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
