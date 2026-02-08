import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  Plus,
  Search,
  Filter,
  Eye,
  Edit,
  Trash2,
  Calendar,
  BookOpen,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { homeworkService, classService, authService } from '../../services';
import { Homework, HomeworkFilters } from '../../types';
import { format } from 'date-fns';

const HomeworkListPage: React.FC = () => {
  const navigate = useNavigate();
  const userRole = authService.getUserRole();
  const userId = authService.getUserId();

  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<HomeworkFilters>({
    status: 'all',
    class_id: undefined,
    subject_id: undefined,
  });
  const [showFilters, setShowFilters] = useState(false);

  const { data: classes = { items: [], total: 0 } } = useQuery({
    queryKey: ['classes'],
    queryFn: () => classService.getClasses({ limit: 100 }),
  });

  const { data: homework = [], isLoading, refetch } = useQuery({
    queryKey: ['homework-list', filters, userId],
    queryFn: async () => {
      const queryFilters: HomeworkFilters = { ...filters };
      if (userRole === 'teacher') {
        queryFilters.teacher_id = userId!;
      }
      return await homeworkService.getHomeworkList(queryFilters);
    },
  });

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this homework?')) {
      try {
        await homeworkService.deleteHomework(id);
        refetch();
      } catch (error) {
        console.error('Failed to delete homework:', error);
        alert('Failed to delete homework');
      }
    }
  };

  const getStatusBadge = (dueDate: string) => {
    const due = new Date(dueDate);
    const now = new Date();

    if (due < now) {
      return (
        <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-700 rounded-full">
          Past Due
        </span>
      );
    } else if (due.getTime() - now.getTime() < 24 * 60 * 60 * 1000) {
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

  const filteredHomework = homework.filter((hw) =>
    hw.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (hw.description?.toLowerCase() || '').includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Homework</h1>
          <p className="text-gray-600 mt-1">
            {filteredHomework.length} assignment{filteredHomework.length !== 1 ? 's' : ''}
          </p>
        </div>
        {userRole === 'teacher' && (
          <Button
            icon={<Plus className="w-5 h-5" />}
            onClick={() => navigate('/homework/create')}
          >
            Create Homework
          </Button>
        )}
      </div>

      <Card variant="elevated" className="p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search homework..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <Button
            variant="secondary"
            icon={<Filter className="w-5 h-5" />}
            onClick={() => setShowFilters(!showFilters)}
          >
            Filters
          </Button>
        </div>

        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={filters.status || 'all'}
                onChange={(e) =>
                  setFilters({ ...filters, status: e.target.value as any })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="all">All</option>
                <option value="active">Active</option>
                <option value="past_due">Past Due</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Class
              </label>
              <select
                value={filters.class_id || ''}
                onChange={(e) =>
                  setFilters({ ...filters, class_id: e.target.value || undefined })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">All Classes</option>
                {classes.items.map((cls) => (
                  <option key={cls.id} value={cls.id}>
                    {cls.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <Button
                variant="ghost"
                fullWidth
                onClick={() =>
                  setFilters({
                    status: 'all',
                    class_id: undefined,
                    subject_id: undefined,
                  })
                }
              >
                Clear Filters
              </Button>
            </div>
          </div>
        )}
      </Card>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : filteredHomework.length > 0 ? (
        <div className="grid grid-cols-1 gap-4">
          {filteredHomework.map((hw) => (
            <Card key={hw.id} variant="elevated" className="p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold text-gray-900">{hw.title}</h3>
                    {getStatusBadge(hw.due_date)}
                  </div>
                  {hw.description && (
                    <p className="text-gray-600 mb-3 line-clamp-2">{hw.description}</p>
                  )}
                  <div className="flex items-center gap-6 text-sm text-gray-500">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      <span>Due: {format(new Date(hw.due_date), 'MMM dd, yyyy')}</span>
                    </div>
                    {hw.page_numbers && (
                      <div className="flex items-center gap-1">
                        <BookOpen className="w-4 h-4" />
                        <span>Pages: {hw.page_numbers}</span>
                      </div>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  <Button
                    size="sm"
                    variant="ghost"
                    icon={<Eye className="w-4 h-4" />}
                    onClick={() => navigate(`/homework/${hw.id}`)}
                  >
                    View
                  </Button>
                  {userRole === 'teacher' && (
                    <>
                      <Button
                        size="sm"
                        variant="ghost"
                        icon={<Edit className="w-4 h-4" />}
                        onClick={() => navigate(`/homework/${hw.id}/edit`)}
                      >
                        Edit
                      </Button>
                      <Button
                        size="sm"
                        variant="danger"
                        icon={<Trash2 className="w-4 h-4" />}
                        onClick={() => handleDelete(hw.id)}
                      >
                        Delete
                      </Button>
                    </>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card variant="elevated" className="p-12 text-center">
          <BookOpen className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No homework found
          </h3>
          <p className="text-gray-500 mb-6">
            {searchQuery || filters.class_id
              ? 'Try adjusting your search or filters'
              : 'Get started by creating your first homework assignment'}
          </p>
          {userRole === 'teacher' && !searchQuery && (
            <Button
              icon={<Plus className="w-5 h-5" />}
              onClick={() => navigate('/homework/create')}
            >
              Create Homework
            </Button>
          )}
        </Card>
      )}
    </div>
  );
};

export default HomeworkListPage;
