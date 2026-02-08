import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  BookOpen,
  Clock,
  CheckCircle,
  TrendingUp,
  User,
  Calendar,
  MessageSquare,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import { LineChart } from '../../components/common/Charts';
import { authService, homeworkService, submissionService, analyticsService } from '../../services';
import { format } from 'date-fns';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  bgColor: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color, bgColor }) => (
  <Card variant="elevated" className="p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-600 mb-1">{title}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
      </div>
      <div className={`p-4 rounded-full ${bgColor}`}>
        <div className={color}>{icon}</div>
      </div>
    </div>
  </Card>
);

interface HomeworkItemProps {
  homework: any;
  submission?: any;
}

const HomeworkItem: React.FC<HomeworkItemProps> = ({ homework, submission }) => {
  const getStatusBadge = () => {
    if (submission?.status === 'graded') {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
          Graded
        </span>
      );
    } else if (submission) {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-700 rounded-full">
          Submitted
        </span>
      );
    } else {
      const dueDate = new Date(homework.due_date);
      const now = new Date();
      if (dueDate < now) {
        return (
          <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-700 rounded-full">
            Overdue
          </span>
        );
      } else {
        return (
          <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-700 rounded-full">
            Pending
          </span>
        );
      }
    }
  };

  return (
    <div className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0">
      <div className="flex-1">
        <h4 className="font-medium text-gray-900">{homework.title}</h4>
        <p className="text-sm text-gray-500 mt-1">
          Due: {format(new Date(homework.due_date), 'MMM dd, yyyy')}
        </p>
      </div>
      <div className="flex items-center gap-4">
        {submission?.grade !== undefined && (
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{submission.grade}</p>
            <p className="text-xs text-gray-500">Grade</p>
          </div>
        )}
        {getStatusBadge()}
      </div>
    </div>
  );
};

interface FeedbackItemProps {
  submission: any;
}

const FeedbackItem: React.FC<FeedbackItemProps> = ({ submission }) => {
  return (
    <div className="p-4 bg-blue-50 border border-blue-100 rounded-lg">
      <div className="flex items-start gap-3">
        <div className="p-2 bg-blue-100 rounded-full">
          <MessageSquare className="w-4 h-4 text-blue-600" />
        </div>
        <div className="flex-1">
          <h4 className="font-medium text-gray-900 text-sm">
            {submission.homework_title || 'Homework'}
          </h4>
          <p className="text-sm text-gray-600 mt-1">{submission.teacher_feedback}</p>
          <p className="text-xs text-gray-500 mt-2">
            {format(new Date(submission.reviewed_at || submission.updated_at), 'MMM dd, yyyy')}
          </p>
        </div>
        {submission.grade !== undefined && (
          <div className="text-center">
            <p className="text-xl font-bold text-blue-600">{submission.grade}</p>
            <p className="text-xs text-gray-500">Grade</p>
          </div>
        )}
      </div>
    </div>
  );
};

const ParentDashboard: React.FC = () => {
  const parentId = authService.getUserId();
  const [selectedChildId, setSelectedChildId] = useState<string>('');

  const { data: children = [] } = useQuery({
    queryKey: ['parent-children', parentId],
    queryFn: async () => {
      return [];
    },
    enabled: !!parentId,
  });

  React.useEffect(() => {
    if (children.length > 0 && !selectedChildId) {
      setSelectedChildId(children[0].id);
    }
  }, [children, selectedChildId]);

  const { data: studentStats, isLoading: statsLoading } = useQuery({
    queryKey: ['student-stats', selectedChildId],
    queryFn: () => analyticsService.getStudentStats(selectedChildId),
    enabled: !!selectedChildId,
  });

  const { data: homework = [] } = useQuery({
    queryKey: ['child-homework', selectedChildId],
    queryFn: async () => {
      return await homeworkService.getHomeworkList({
        limit: 10,
      });
    },
    enabled: !!selectedChildId,
  });

  const { data: submissions = [] } = useQuery({
    queryKey: ['child-submissions', selectedChildId],
    queryFn: async () => {
      return await submissionService.getSubmissions({
        student_id: selectedChildId,
        limit: 50,
      });
    },
    enabled: !!selectedChildId,
  });

  const { data: performanceTrend = [] } = useQuery({
    queryKey: ['performance-trend', selectedChildId],
    queryFn: () => analyticsService.getStudentPerformanceTrend(selectedChildId),
    enabled: !!selectedChildId,
  });

  const submissionsByHomework = new Map(
    submissions.map((sub) => [sub.homework_id, sub])
  );

  const recentFeedback = submissions
    .filter((sub) => sub.teacher_feedback && sub.teacher_feedback.trim() !== '')
    .slice(0, 3);

  const chartData = performanceTrend.map((item: any) => ({
    date: format(new Date(item.date), 'MMM dd'),
    Grade: item.average_grade,
  }));

  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Parent Dashboard</h1>
        <p className="text-gray-600 mt-1">Monitor your child's progress</p>
      </div>

      {children.length > 1 && (
        <Card variant="elevated" className="p-4">
          <div className="flex items-center gap-3">
            <User className="w-5 h-5 text-gray-400" />
            <select
              value={selectedChildId}
              onChange={(e) => setSelectedChildId(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              {children.map((child: any) => (
                <option key={child.id} value={child.id}>
                  {child.first_name} {child.last_name}
                </option>
              ))}
            </select>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Homework"
          value={studentStats?.total_homework || 0}
          icon={<BookOpen className="w-6 h-6" />}
          color="text-blue-600"
          bgColor="bg-blue-100"
        />
        <StatCard
          title="Pending"
          value={studentStats?.pending_homework || 0}
          icon={<Clock className="w-6 h-6" />}
          color="text-yellow-600"
          bgColor="bg-yellow-100"
        />
        <StatCard
          title="Completed"
          value={studentStats?.completed_homework || 0}
          icon={<CheckCircle className="w-6 h-6" />}
          color="text-green-600"
          bgColor="bg-green-100"
        />
        <StatCard
          title="Average Grade"
          value={studentStats?.average_grade?.toFixed(1) || '-'}
          icon={<TrendingUp className="w-6 h-6" />}
          color="text-purple-600"
          bgColor="bg-purple-100"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Grade Trends</h2>
            </Card.Header>
            <Card.Body>
              {chartData.length > 0 ? (
                <LineChart
                  data={chartData}
                  xAxisKey="date"
                  dataKey="Grade"
                  color="#8B5CF6"
                  height={300}
                />
              ) : (
                <div className="flex items-center justify-center h-64 text-gray-400">
                  No data available
                </div>
              )}
            </Card.Body>
          </Card>
        </div>

        <div>
          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Quick Stats</h2>
            </Card.Header>
            <Card.Body>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Completion Rate</span>
                  <span className="text-lg font-bold text-gray-900">
                    {studentStats?.completion_rate?.toFixed(0) || 0}%
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">On-Time</span>
                  <span className="text-lg font-bold text-gray-900">
                    {studentStats?.on_time_submissions || 0}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Late</span>
                  <span className="text-lg font-bold text-gray-900">
                    {studentStats?.late_submissions || 0}
                  </span>
                </div>
              </div>
            </Card.Body>
          </Card>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card variant="elevated">
          <Card.Header divider>
            <h2 className="text-xl font-bold text-gray-900">Homework Overview</h2>
          </Card.Header>
          <div>
            {homework.length > 0 ? (
              homework.map((hw) => (
                <HomeworkItem
                  key={hw.id}
                  homework={hw}
                  submission={submissionsByHomework.get(hw.id)}
                />
              ))
            ) : (
              <div className="p-8 text-center text-gray-500">
                <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No homework assigned</p>
              </div>
            )}
          </div>
        </Card>

        <Card variant="elevated">
          <Card.Header divider>
            <h2 className="text-xl font-bold text-gray-900">Recent Teacher Feedback</h2>
          </Card.Header>
          <Card.Body>
            {recentFeedback.length > 0 ? (
              <div className="space-y-3">
                {recentFeedback.map((submission) => (
                  <FeedbackItem key={submission.id} submission={submission} />
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <MessageSquare className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No teacher feedback yet</p>
              </div>
            )}
          </Card.Body>
        </Card>
      </div>
    </div>
  );
};

export default ParentDashboard;
