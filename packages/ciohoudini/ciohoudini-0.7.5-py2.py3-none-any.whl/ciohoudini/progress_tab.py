""" Progress bar """


from ciohoudini import payload
from ciohoudini.buttoned_scroll_panel import ButtonedScrollPanel

from ciohoudini.progress.md5_progress_widget import MD5ProgressWidget
from ciohoudini.progress.upload_progress_widget import UploadProgressWidget
from ciohoudini.progress.jobs_progress_widget import JobsProgressWidget

from ciohoudini.progress.file_status_panel import FileStatusPanel
from ciohoudini.progress.submission_worker import SubmissionWorkerBase

import logging

from PySide2.QtCore import QThreadPool


logger = logging.getLogger(__name__)


class ProgressTab(ButtonedScrollPanel):
    """The progress tab.

    Shows the progress of the submissions with 4 elements:

    1. Jobs progress: Shows the progress of the entire batch of jobs.
    2. MD5 progress: Shows the progress of the MD5 generation for the current job.
    3. Upload progress: Shows the progress of the upload for the current job.
    4. File status: Shows detailed progress for each file.

    """

    def __init__(self, dialog):
        super(ProgressTab, self).__init__(
            dialog, buttons=[("cancel", "Cancel")]
        )

        self.progress_list = []
        self.responses = []

        self.jobs_widget = JobsProgressWidget()
        self.md5_widget = MD5ProgressWidget()
        self.upload_widget = UploadProgressWidget()
        self.file_status_panel = FileStatusPanel()

        self.layout.addWidget(self.jobs_widget)
        self.layout.addWidget(self.md5_widget)
        self.layout.addWidget(self.upload_widget)
        self.layout.addWidget(self.file_status_panel)

        self.buttons["cancel"].clicked.connect(self.on_cancel_button)
        # self.buttons["cancel"].clicked.connect(self.dialog.on_close())

    def get_submission_payload(self, node):
        """Get the submission payload for the given node."""
        kwargs = {}
        kwargs["do_asset_scan"] = True
        kwargs["task_limit"] = -1
        submission_payload = payload.resolve_payload(node, **kwargs)
        return submission_payload

    def submit(self, node):
        """Submits the jobs.

        Send the submission generator to the worker.
        """

        self.jobs_widget.reset()
        self.md5_widget.reset()
        self.upload_widget.reset()
        self.file_status_panel.reset()

        self.responses = []

        self.mock_file = None
        self.use_mock = None
        self.mock_frequency = None

        submissions = self.get_submission_payload(node)

        if not submissions:
            logger.info("No submissions found")
            return

        job_count = len(submissions)

        self.threadpool = QThreadPool()

        self.worker = SubmissionWorkerBase.create(
            submissions,
            job_count,
            self.use_mock,
            self.mock_file,
            self.mock_frequency,
        )
        self.worker.signals.on_start.connect(self.jobs_widget.reset)
        self.worker.signals.on_job_start.connect(self.md5_widget.reset)
        self.worker.signals.on_job_start.connect(self.upload_widget.reset)
        self.worker.signals.on_progress.connect(self.md5_widget.set_progress)
        self.worker.signals.on_progress.connect(self.upload_widget.set_progress)
        self.worker.signals.on_progress.connect(self.jobs_widget.set_progress)
        self.worker.signals.on_progress.connect(self.file_status_panel.set_progress)
        self.worker.signals.on_response.connect(self.handle_response)
        self.worker.signals.on_done.connect(self.handle_done)
        self.worker.signals.on_error.connect(self.handle_error)

        self.threadpool.start(self.worker)

    def handle_response(self, response):
        """Handle the job submitted response.

        We add in some extra information to help identify the job within the batch.
        """
        self.responses.append(response)

    def handle_error(self, error):
        """Make an error string from the exception and push it onto the responses."""
        self.responses.append(error)

    def on_cancel_button(self):
        if self.worker:
            self.worker.cancel()
        self.dialog.on_close()


    def handle_done(self):

        self.dialog.tab_widget.setCurrentWidget(self.dialog.response_tab)

        # Enable response tab and disable validation and progress tabs
        self.dialog.tab_widget.setTabEnabled(2, True)
        self.dialog.tab_widget.setTabEnabled(0, False)
        #self.dialog.tab_widget.setTabEnabled(1, False)

        self.dialog.response_tab.hydrate(self.responses)
        #self.dialog.response_tab.populate(self.responses)
