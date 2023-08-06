
from ciohoudini.buttoned_scroll_panel import ButtonedScrollPanel
from ciohoudini.notice_grp import NoticeGrp
from ciohoudini import submit


class ValidationTab(ButtonedScrollPanel):

    def __init__(self, dialog):
        super(ValidationTab, self).__init__(
            dialog,
            buttons=[("close", "Close"), ("continue", "Continue Submission")])
        self.dialog = dialog
        self.configure_signals()

    def configure_signals(self):
        self.buttons["close"].clicked.connect(self.dialog.on_close)
        self.buttons["continue"].clicked.connect(self.on_continue)

    def populate(self, errors, warnings, infos):
        
        obj = {
            "error": errors,
            "warning": warnings,
            "info": infos
        }
        has_issues = False
        for severity in ["error", "warning", "info"]:
            for entry in obj[severity]:
                has_issues = True
                widget = NoticeGrp(entry, severity)
                self.layout.addWidget(widget)

        if not has_issues:
            widget = NoticeGrp("No issues found", "success")
            self.layout.addWidget(widget)

        self.layout.addStretch()

        self.buttons["continue"].setEnabled(not errors)

    def on_continue(self):
        """ When someone clicks on Continue Submission """
        nodes = self.dialog.nodes
        node = nodes[0] if nodes else None

        self.dialog.tab_widget.setCurrentWidget(self.dialog.progress_tab)

        # Enable progress and disable validation and response tabs
        self.dialog.tab_widget.setTabEnabled(1, True)
        self.dialog.tab_widget.setTabEnabled(0, False)
        self.dialog.tab_widget.setTabEnabled(2, False)

        self.dialog.progress_tab.submit(node)

        #results = submit.run(*(self.dialog.nodes))
        
 