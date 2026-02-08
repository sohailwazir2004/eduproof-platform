import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  BookOpen,
  FileText,
  CheckCircle,
  Clock,
  TrendingUp,
  Plus,
  Eye,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { LineChart } from '../../components/common/Charts';
import { authService, homeworkService, submissionService, analyticsService } from '../../services';
import { Homework, Submission } from '../../types';
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

const HomeworkRow: React.FC<{ homework: Homework & { submission_count?: number } }> = ({
  homework,
}) => {
  const navigate = useNavigate();

  const getStatusBadge = () => {
    const dueDate = new Date(homework.due_date);
    const now = new Date();

    if (dueDate < now) {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-700 rounded-full">
          Past Due
        </span>
      );
    } else if (dueDate.getTime() - now.getTime() < 24 * 60 * 60 * 1000) {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-700 rounded-full">
          Due Soon
        </span>
      );
    } else {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
          Active
        </span>
      );
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
        <div className="text-center">
          <p className="text-2xl font-bold text-gray-900">
            {homework.submission_count || 0}
          </p>
          <p className="text-xs text-gray-500">Submissions</p>
        </div>
        {getStatusBadge()}
        <Button
          size="sm"
          variant="ghost"
          icon={<Eye className="w-4 h-4" />}
          onClick={() => navigate(`/homework/${homework.id}`)}
        >
          View
        </Button>
      </div>
    </div>
  );
};

const TeacherDashboard: React.FC = () => {
  const navigate = useNavigate();
  const teacherId = authService.getUserId();

  const { data: teacherStats, isLoading: statsLoading } = useQuery({
    queryKey: ['teacher-stats', teacherId],
    queryFn: () => analyticsService.getTeacherStats(teacherId!),
    enabled: !!teacherId,
  });

  const { data: recentHomework = [], isLoading: homeworkLoading } = useQuery({
    queryKey: ['recent-homework', teacherId],
    queryFn: async () => {
      const homework = await homeworkService.getHomeworkList({
        teacher_id: teacherId!,
        limit: 5,
      });

      const homeworkWithSubmissions = await Promise.all(
        homework.map(async (hw) => {
          try {
            const submissions = await homeworkService.getHomeworkSubmissions(hw.id);
            return { ...hw, submission_count: submissions.length };
          } catch {
            return { ...hw, submission_count: 0 };
          }
        })
      );

      return homeworkWithSubmissions;
    },
    enabled: !!teacherId,
  });

  const { data: pendingSubmissions = [], isLoading: submissionsLoading } = useQuery({
    queryKey: ['pending-submissions', teacherId],
    queryFn: async () => {
      return await submissionService.getSubmissions({
        status: 'pending',
        limit: 10,
      });
    },
  });

  const { data: completionData = [] } = useQuery({
    queryKey: ['homework-completion', teacherId],
    queryFn: async () => {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30);

      return await analyticsService.getHomeworkCompletionRates(
        startDate.toISOString(),
        endDate.toISOString()
      );
    },
    enabled: !!teacherId,
  });

  const chartData = completionData.map((item) => ({
    date: format(new Date(item.date), 'MMM dd'),
    'Completion Rate': item.completion_rate,
  }));

  const todayGraded = pendingSubmissions.filter(
    (sub) =>
      sub.status === 'graded' &&
      new Date(sub.reviewed_at || '').toDateString() === new Date().toDateString()
  ).length;

  if (statsLoading || homeworkLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Teacher Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back! Here's your overview.</p>
        </div>
        <Button
          icon={<Plus className="w-5 h-5" />}
          onClick={() => navigate('/homework/create')}
        >
          Create Homework
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Homework"
          value={teacherStats?.total_homework_assigned || 0}
          icon={<BookOpen className="w-6 h-6" />}
          color="text-blue-600"
          bgColor="bg-blue-100"
        />
        <StatCard
          title="Pending Submissions"
          value={pendingSubmissions.length}
          icon={<Clock className="w-6 h-6" />}
          color="text-yellow-600"
          bgColor="bg-yellow-100"
        />
        <StatCard
          title="Graded Today"
          value={todayGraded}
          icon={<CheckCircle className="w-6 h-6" />}
          color="text-green-600"
          bgColor="bg-green-100"
        />
        <StatCard
          title="Total Classes"
          value={teacherStats?.total_classes || 0}
          icon={<FileText className="w-6 h-6" />}
          color="text-purple-600"
          bgColor="bg-purple-100"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card variant="elevated">
            <Card.Header divider>
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-gray-900">
                    Submission Trends
                  </h2>
                  <p className="text-sm text-gray-500 mt-1">Last 30 days</p>
                </div>
                <TrendingUp className="w-5 h-5 text-gray-400" />
              </div>
            </Card.Header>
            <Card.Body>
              {chartData.length > 0 ? (
                <LineChart
                  data={chartData}
                  xAxisKey="date"
                  dataKey="Completion Rate"
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
              <h2 className="text-xl font-bold text-gray-900">Quick Actions</h2>
            </Card.Header>
            <Card.Body>
              <div className="space-y-3">
                <Button
                  fullWidth
                  variant="primary"
                  icon={<Plus className="w-5 h-5" />}
                  onClick={() => navigate('/homework/create')}
                >
                  Create Homework
                </Button>
                <Button
                  fullWidth
                  variant="secondary"
                  icon={<FileText className="w-5 h-5" />}
                  onClick={() => navigate('/submissions')}
                >
                  View Submissions
                </Button>
                <Button
                  fullWidth
                  variant="secondary"
                  icon={<BookOpen className="w-5 h-5" />}
                  onClick={() => navigate('/textbooks')}
                >
                  Manage Textbooks
                </Button>
                <Button
                  fullWidth
                  variant="ghost"
                  icon={<TrendingUp className="w-5 h-5" />}
                  onClick={() => navigate('/analytics')}
                >
                  View Analytics
                </Button>
              </div>
            </Card.Body>
          </Card>
        </div>
      </div>

      <Card variant="elevated">
        <Card.Header divider>
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">Recent Homework</h2>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => navigate('/homework')}
            >
              View All
            </Button>
          </div>
        </Card.Header>
        <div>
          {recentHomework.length > 0 ? (
            recentHomework.map((homework) => (
              <HomeworkRow key={homework.id} homework={homework} />
            ))
          ) : (
            <div className="p-8 text-center text-gray-500">
              <BookOpen className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p>No homework assigned yet</p>
              <Button
                size="sm"
                variant="primary"
                icon={<Plus className="w-4 h-4" />}
                onClick={() => navigate('/homework/create')}
                className="mt-4"
              >
                Create Your First Homework
              </Button>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export default TeacherDashboard;
