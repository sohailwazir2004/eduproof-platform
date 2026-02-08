import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  Users,
  BookOpen,
  GraduationCap,
  TrendingUp,
  Award,
  Activity,
  BarChart3,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { MultiBarChart, DonutChart } from '../../components/common/Charts';
import { analyticsService, classService } from '../../services';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  bgColor: string;
  subtitle?: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color, bgColor, subtitle }) => (
  <Card variant="elevated" className="p-6">
    <div className="flex items-center justify-between mb-2">
      <div>
        <p className="text-sm text-gray-600 mb-1">{title}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
        {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
      </div>
      <div className={`p-4 rounded-full ${bgColor}`}>
        <div className={color}>{icon}</div>
      </div>
    </div>
  </Card>
);

interface ClassPerformanceRowProps {
  classData: any;
  rank: number;
}

const ClassPerformanceRow: React.FC<ClassPerformanceRowProps> = ({ classData, rank }) => {
  const getRankBadge = () => {
    if (rank === 1) {
      return (
        <div className="flex items-center gap-1 px-2 py-1 bg-yellow-100 rounded-full">
          <Award className="w-4 h-4 text-yellow-600" />
          <span className="text-xs font-medium text-yellow-700">1st</span>
        </div>
      );
    } else if (rank === 2) {
      return (
        <div className="flex items-center gap-1 px-2 py-1 bg-gray-100 rounded-full">
          <Award className="w-4 h-4 text-gray-600" />
          <span className="text-xs font-medium text-gray-700">2nd</span>
        </div>
      );
    } else if (rank === 3) {
      return (
        <div className="flex items-center gap-1 px-2 py-1 bg-orange-100 rounded-full">
          <Award className="w-4 h-4 text-orange-600" />
          <span className="text-xs font-medium text-orange-700">3rd</span>
        </div>
      );
    } else {
      return (
        <span className="text-sm font-medium text-gray-600">#{rank}</span>
      );
    }
  };

  const getGradeColor = (grade: number) => {
    if (grade >= 90) return 'text-green-600';
    if (grade >= 80) return 'text-blue-600';
    if (grade >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0">
      <div className="flex items-center gap-4 flex-1">
        {getRankBadge()}
        <div>
          <h4 className="font-medium text-gray-900">{classData.class_name}</h4>
          <p className="text-sm text-gray-500">
            {classData.total_students} students • {classData.total_homework} homework
          </p>
        </div>
      </div>
      <div className="flex items-center gap-6">
        <div className="text-center">
          <p className={`text-2xl font-bold ${getGradeColor(classData.average_grade)}`}>
            {classData.average_grade?.toFixed(1) || '-'}
          </p>
          <p className="text-xs text-gray-500">Avg Grade</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-gray-900">
            {classData.submission_rate?.toFixed(0) || 0}%
          </p>
          <p className="text-xs text-gray-500">Completion</p>
        </div>
      </div>
    </div>
  );
};

const PrincipalDashboard: React.FC = () => {
  const navigate = useNavigate();

  const { data: schoolStats, isLoading: statsLoading } = useQuery({
    queryKey: ['school-stats'],
    queryFn: () => analyticsService.getSchoolStats(),
  });

  const { data: classesData } = useQuery({
    queryKey: ['all-classes'],
    queryFn: () => classService.getClasses({ limit: 100 }),
  });

  const { data: classStats = [] } = useQuery({
    queryKey: ['all-class-stats'],
    queryFn: async () => {
      if (!classesData?.items) return [];
      const stats = await Promise.all(
        classesData.items.map((cls) =>
          analyticsService.getClassStats(cls.id).catch(() => null)
        )
      );
      return stats.filter((s) => s !== null);
    },
    enabled: !!classesData?.items,
  });

  const { data: gradeDistribution = [] } = useQuery({
    queryKey: ['grade-distribution'],
    queryFn: () => analyticsService.getGradeDistribution(),
  });

  const { data: completionData = [] } = useQuery({
    queryKey: ['school-completion-rates'],
    queryFn: async () => {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30);
      return await analyticsService.getHomeworkCompletionRates(
        startDate.toISOString(),
        endDate.toISOString()
      );
    },
  });

  const sortedClasses = [...classStats].sort(
    (a, b) => (b.average_grade || 0) - (a.average_grade || 0)
  );

  const topClasses = sortedClasses.slice(0, 5);

  const completionChartData = completionData.slice(-7).map((item) => {
    const date = new Date(item.date);
    return {
      date: `${date.getMonth() + 1}/${date.getDate()}`,
      Assigned: item.assigned,
      Completed: item.completed,
    };
  });

  const completionRateData = [
    {
      name: 'Completed',
      value: schoolStats?.total_submissions || 0,
    },
    {
      name: 'Pending',
      value: (schoolStats?.active_homework || 0) - (schoolStats?.total_submissions || 0),
    },
  ];

  if (statsLoading) {
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
          <h1 className="text-3xl font-bold text-gray-900">Principal Dashboard</h1>
          <p className="text-gray-600 mt-1">School-wide analytics and performance</p>
        </div>
        <Button
          icon={<BarChart3 className="w-5 h-5" />}
          onClick={() => navigate('/analytics')}
        >
          Full Analytics
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Students"
          value={schoolStats?.total_students || 0}
          icon={<Users className="w-6 h-6" />}
          color="text-blue-600"
          bgColor="bg-blue-100"
        />
        <StatCard
          title="Total Teachers"
          value={schoolStats?.total_teachers || 0}
          icon={<GraduationCap className="w-6 h-6" />}
          color="text-purple-600"
          bgColor="bg-purple-100"
        />
        <StatCard
          title="Total Classes"
          value={schoolStats?.total_classes || 0}
          icon={<BookOpen className="w-6 h-6" />}
          color="text-green-600"
          bgColor="bg-green-100"
        />
        <StatCard
          title="Average Grade"
          value={schoolStats?.overall_average_grade?.toFixed(1) || '-'}
          icon={<TrendingUp className="w-6 h-6" />}
          color="text-orange-600"
          bgColor="bg-orange-100"
          subtitle={`${schoolStats?.overall_completion_rate?.toFixed(0) || 0}% completion`}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card variant="elevated">
            <Card.Header divider>
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-gray-900">
                    Homework Completion Trend
                  </h2>
                  <p className="text-sm text-gray-500 mt-1">Last 7 days</p>
                </div>
                <Activity className="w-5 h-5 text-gray-400" />
              </div>
            </Card.Header>
            <Card.Body>
              {completionChartData.length > 0 ? (
                <MultiBarChart
                  data={completionChartData}
                  xAxisKey="date"
                  bars={[
                    { dataKey: 'Assigned', name: 'Assigned', color: '#3B82F6' },
                    { dataKey: 'Completed', name: 'Completed', color: '#10B981' },
                  ]}
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
              <h2 className="text-xl font-bold text-gray-900">Completion Rate</h2>
            </Card.Header>
            <Card.Body>
              {completionRateData.some((d) => d.value > 0) ? (
                <DonutChart
                  data={completionRateData}
                  dataKey="value"
                  nameKey="name"
                  height={250}
                />
              ) : (
                <div className="flex items-center justify-center h-64 text-gray-400">
                  No data available
                </div>
              )}
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Pending Reviews</span>
                  <span className="text-lg font-bold text-gray-900">
                    {schoolStats?.pending_reviews || 0}
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
            <h2 className="text-xl font-bold text-gray-900">Top Performing Classes</h2>
          </Card.Header>
          <div>
            {topClasses.length > 0 ? (
              topClasses.map((classData, index) => (
                <ClassPerformanceRow
                  key={classData.class_id}
                  classData={classData}
                  rank={index + 1}
                />
              ))
            ) : (
              <div className="p-8 text-center text-gray-500">
                <BarChart3 className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No class data available</p>
              </div>
            )}
          </div>
        </Card>

        <Card variant="elevated">
          <Card.Header divider>
            <h2 className="text-xl font-bold text-gray-900">Quick Insights</h2>
          </Card.Header>
          <Card.Body>
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 border border-blue-100 rounded-lg">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-blue-100 rounded-full">
                    <TrendingUp className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Active Homework</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {schoolStats?.active_homework || 0} homework assignments currently active
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-green-50 border border-green-100 rounded-lg">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-green-100 rounded-full">
                    <Users className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Total Submissions</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {schoolStats?.total_submissions || 0} submissions received
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-purple-50 border border-purple-100 rounded-lg">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-purple-100 rounded-full">
                    <Award className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Overall Performance</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      School average grade: {schoolStats?.overall_average_grade?.toFixed(1) || '-'}
                    </p>
                  </div>
                </div>
              </div>

              <Button
                fullWidth
                variant="secondary"
                icon={<BarChart3 className="w-5 h-5" />}
                onClick={() => navigate('/analytics')}
              >
                View Detailed Analytics
              </Button>
            </div>
          </Card.Body>
        </Card>
      </div>
    </div>
  );
};

export default PrincipalDashboard;
