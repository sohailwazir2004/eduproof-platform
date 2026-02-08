import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  BookOpen,
  Clock,
  CheckCircle,
  AlertCircle,
  Upload,
  TrendingUp,
  Calendar,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { DonutChart } from '../../components/common/Charts';
import { authService, homeworkService, submissionService, analyticsService } from '../../services';
import { Homework } from '../../types';
import { format, differenceInDays } from 'date-fns';

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

interface HomeworkCardProps {
  homework: Homework;
  hasSubmission: boolean;
}

const HomeworkCard: React.FC<HomeworkCardProps> = ({ homework, hasSubmission }) => {
  const navigate = useNavigate();
  const daysUntilDue = differenceInDays(new Date(homework.due_date), new Date());

  const getUrgencyStyle = () => {
    if (daysUntilDue < 0) {
      return 'border-red-300 bg-red-50';
    } else if (daysUntilDue <= 1) {
      return 'border-yellow-300 bg-yellow-50';
    } else {
      return 'border-gray-200 bg-white';
    }
  };

  const getUrgencyBadge = () => {
    if (daysUntilDue < 0) {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-700 rounded-full">
          Overdue
        </span>
      );
    } else if (daysUntilDue === 0) {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-orange-100 text-orange-700 rounded-full">
          Due Today
        </span>
      );
    } else if (daysUntilDue === 1) {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-700 rounded-full">
          Due Tomorrow
        </span>
      );
    } else {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
          {daysUntilDue} days left
        </span>
      );
    }
  };

  return (
    <Card variant="bordered" className={`${getUrgencyStyle()} transition-all hover:shadow-md`}>
      <div className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 text-lg">{homework.title}</h3>
            {homework.description && (
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">{homework.description}</p>
            )}
          </div>
          {getUrgencyBadge()}
        </div>

        <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            <span>Due: {format(new Date(homework.due_date), 'MMM dd, yyyy')}</span>
          </div>
        </div>

        {hasSubmission ? (
          <div className="flex items-center gap-2 text-green-600 text-sm font-medium">
            <CheckCircle className="w-4 h-4" />
            <span>Submitted</span>
          </div>
        ) : (
          <Button
            fullWidth
            size="sm"
            variant="primary"
            icon={<Upload className="w-4 h-4" />}
            onClick={() => navigate(`/homework/${homework.id}/submit`)}
          >
            Submit Homework
          </Button>
        )}
      </div>
    </Card>
  );
};

interface RecentGradeProps {
  submission: any;
}

const RecentGrade: React.FC<RecentGradeProps> = ({ submission }) => {
  const getGradeColor = (grade: number) => {
    if (grade >= 90) return 'text-green-600';
    if (grade >= 80) return 'text-blue-600';
    if (grade >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0">
      <div className="flex-1">
        <h4 className="font-medium text-gray-900">{submission.homework_title || 'Homework'}</h4>
        <p className="text-sm text-gray-500 mt-1">
          Submitted: {format(new Date(submission.submitted_at), 'MMM dd, yyyy')}
        </p>
        {submission.teacher_feedback && (
          <p className="text-sm text-gray-600 mt-1 line-clamp-2">
            {submission.teacher_feedback}
          </p>
        )}
      </div>
      <div className="text-center ml-4">
        <p className={`text-3xl font-bold ${getGradeColor(submission.grade || 0)}`}>
          {submission.grade !== undefined ? submission.grade : '-'}
        </p>
        <p className="text-xs text-gray-500">Grade</p>
      </div>
    </div>
  );
};

const StudentDashboard: React.FC = () => {
  const navigate = useNavigate();
  const studentId = authService.getUserId();

  const { data: studentStats, isLoading: statsLoading } = useQuery({
    queryKey: ['student-stats', studentId],
    queryFn: () => analyticsService.getStudentStats(studentId!),
    enabled: !!studentId,
  });

  const { data: upcomingHomework = [], isLoading: homeworkLoading } = useQuery({
    queryKey: ['upcoming-homework', studentId],
    queryFn: async () => {
      return await homeworkService.getHomeworkList({
        status: 'active',
        limit: 10,
      });
    },
  });

  const { data: submissions = [] } = useQuery({
    queryKey: ['my-submissions', studentId],
    queryFn: async () => {
      return await submissionService.getSubmissions({
        student_id: studentId!,
        limit: 100,
      });
    },
    enabled: !!studentId,
  });

  const submittedHomeworkIds = new Set(submissions.map((sub) => sub.homework_id));

  const gradedSubmissions = submissions
    .filter((sub) => sub.status === 'graded' && sub.grade !== undefined)
    .slice(0, 5);

  const progressData = [
    {
      name: 'Completed',
      value: studentStats?.completed_homework || 0,
    },
    {
      name: 'Pending',
      value: studentStats?.pending_homework || 0,
    },
  ];

  if (statsLoading || homeworkLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Student Dashboard</h1>
        <p className="text-gray-600 mt-1">Track your homework and grades</p>
      </div>

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
              <h2 className="text-xl font-bold text-gray-900">
                Upcoming Homework
              </h2>
            </Card.Header>
            <div className="p-4 space-y-4">
              {upcomingHomework.length > 0 ? (
                upcomingHomework.map((homework) => (
                  <HomeworkCard
                    key={homework.id}
                    homework={homework}
                    hasSubmission={submittedHomeworkIds.has(homework.id)}
                  />
                ))
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <CheckCircle className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                  <p>No upcoming homework</p>
                  <p className="text-sm mt-1">Great job! You're all caught up!</p>
                </div>
              )}
            </div>
          </Card>
        </div>

        <div>
          <Card variant="elevated" className="mb-6">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Progress</h2>
            </Card.Header>
            <Card.Body>
              {progressData.some((item) => item.value > 0) ? (
                <DonutChart
                  data={progressData}
                  dataKey="value"
                  nameKey="name"
                  height={250}
                />
              ) : (
                <div className="flex items-center justify-center h-64 text-gray-400">
                  No data available
                </div>
              )}
            </Card.Body>
          </Card>

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
                  <span className="text-sm text-gray-600">On-Time Submissions</span>
                  <span className="text-lg font-bold text-gray-900">
                    {studentStats?.on_time_submissions || 0}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Late Submissions</span>
                  <span className="text-lg font-bold text-gray-900">
                    {studentStats?.late_submissions || 0}
                  </span>
                </div>
              </div>
            </Card.Body>
          </Card>
        </div>
      </div>

      <Card variant="elevated">
        <Card.Header divider>
          <h2 className="text-xl font-bold text-gray-900">Recent Grades</h2>
        </Card.Header>
        <div>
          {gradedSubmissions.length > 0 ? (
            gradedSubmissions.map((submission) => (
              <RecentGrade key={submission.id} submission={submission} />
            ))
          ) : (
            <div className="p-8 text-center text-gray-500">
              <AlertCircle className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p>No grades yet</p>
              <p className="text-sm mt-1">Complete homework to receive grades</p>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export default StudentDashboard;
