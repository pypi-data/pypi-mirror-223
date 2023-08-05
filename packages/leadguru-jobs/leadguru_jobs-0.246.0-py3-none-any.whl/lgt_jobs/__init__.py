name = "lgt_jobs"

from .jobs.user_balance_update import UpdateUserBalanceJob, UpdateUserBalanceJobData
from .jobs.conversation_replied import ConversationRepliedJob, ConversationRepliedJobData
from .jobs.reactions_added import ReactionAddedJobData, ReactionAddedJob
from .jobs.send_slack_message import SendSlackMessageJob, SendSlackMessageJobData
from .jobs.user_limits_update import UpdateUserDataUsageJob, UpdateUserDataUsageJobData
from .jobs.analytics import (TrackAnalyticsJob, TrackAnalyticsJobData)
from .jobs.archive_leads import (ArchiveLeadsJob, ArchiveLeadsJobData)
from .jobs.bot_stats_update import (BotStatsUpdateJob, BotStatsUpdateJobData)
from .jobs.chat_history import (LoadChatHistoryJob, LoadChatHistoryJobData)
from .jobs.update_slack_profile import (UpdateUserSlackProfileJob, UpdateUserSlackProfileJobData)
from .jobs.reindex_conversation_history import ReIndexUserLeadsConversationHistoryJob,\
    ReIndexUserLeadsConversationHistoryJobData
from .jobs.clear_user_analytics import ClearUserAnalyticsJobData, ClearUserAnalyticsJob
from .jobs.inbox_leads import InboxLeadsJob, InboxLeadsJobData

from .basejobs import (BaseBackgroundJobData, BaseBackgroundJob, InvalidJobTypeException)
from .smtp import (SendMailJob, SendMailJobData)
from .runner import (BackgroundJobRunner)
from .simple_job import (SimpleTestJob, SimpleTestJobData)

jobs_map = {
    "SimpleTestJob": SimpleTestJob,
    "BotStatsUpdateJob": BotStatsUpdateJob,
    "ArchiveLeadsJob": ArchiveLeadsJob,
    "SendMailJob": SendMailJob,
    "TrackAnalyticsJob": TrackAnalyticsJob,
    "LoadChatHistoryJob": LoadChatHistoryJob,
    "UpdateUserSlackProfileJob": UpdateUserSlackProfileJob,
    "UpdateUserDataUsageJob": UpdateUserDataUsageJob,
    "ConversationRepliedJob": ConversationRepliedJob,
    "ReactionAddedJob": ReactionAddedJob,
    "SendSlackMessageJob": SendSlackMessageJob,
    "UpdateUserBalanceJob": UpdateUserBalanceJob,
    "ReIndexUserLeadsConversationHistoryJob": ReIndexUserLeadsConversationHistoryJob,
    "ClearUserAnalyticsJob": ClearUserAnalyticsJob,
    "InboxLeadsJob": InboxLeadsJob
}
__all__ = [
    # Jobs
    SimpleTestJob,
    BotStatsUpdateJob,
    ArchiveLeadsJob,
    SendMailJob,
    SimpleTestJob,
    LoadChatHistoryJob,
    UpdateUserSlackProfileJob,
    TrackAnalyticsJob,
    UpdateUserDataUsageJob,
    ConversationRepliedJob,
    ReactionAddedJob,
    SendSlackMessageJob,
    UpdateUserBalanceJob,
    ReIndexUserLeadsConversationHistoryJob,
    ClearUserAnalyticsJob,
    InboxLeadsJob,

    # module classes
    BackgroundJobRunner,
    BaseBackgroundJobData,
    BaseBackgroundJob,
    InvalidJobTypeException,
    BotStatsUpdateJobData,
    ArchiveLeadsJobData,
    SendMailJobData,
    SimpleTestJobData,
    LoadChatHistoryJobData,
    UpdateUserSlackProfileJobData,
    TrackAnalyticsJobData,
    UpdateUserDataUsageJobData,
    ConversationRepliedJobData,
    ReactionAddedJobData,
    SendSlackMessageJobData,
    UpdateUserBalanceJobData,
    ReIndexUserLeadsConversationHistoryJobData,
    ClearUserAnalyticsJobData,
    InboxLeadsJobData,

    # mapping
    jobs_map
]
