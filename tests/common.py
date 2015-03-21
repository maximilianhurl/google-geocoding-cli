from mock import patch


class PathExistsMockMixin(object):

    def setUp(self):
        super(PathExistsMockMixin, self).setUp()
        self.patcher = patch('scripts.files.os.path.exists')
        self.path_exists = self.patcher.start()

    def tearDown(self):
        super(PathExistsMockMixin, self).setUp()
        self.patcher.stop()
