import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ArrowLeft, Save, Send } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import FileUpload from '../../components/common/FileUpload';
import { homeworkService, classService, textbookService } from '../../services';
import { HomeworkCreate } from '../../types';

const homeworkSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().optional(),
  class_id: z.string().min(1, 'Class is required'),
  subject_id: z.string().optional(),
  textbook_id: z.string().optional(),
  page_numbers: z.string().optional(),
  due_date: z.string().min(1, 'Due date is required'),
});

type HomeworkFormData = z.infer<typeof homeworkSchema>;

const CreateHomeworkPage: React.FC = () => {
  const navigate = useNavigate();
  const [attachedFiles, setAttachedFiles] = useState<File[]>([]);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<HomeworkFormData>({
    resolver: zodResolver(homeworkSchema),
    defaultValues: {
      title: '',
      description: '',
      class_id: '',
      subject_id: '',
      textbook_id: '',
      page_numbers: '',
      due_date: '',
    },
  });

  const { data: classes = { items: [], total: 0 } } = useQuery({
    queryKey: ['classes'],
    queryFn: () => classService.getClasses({ limit: 100 }),
  });

  const { data: textbooks = [] } = useQuery({
    queryKey: ['textbooks'],
    queryFn: async () => {
      try {
        return await textbookService.getTextbooks({ limit: 100 });
      } catch {
        return [];
      }
    },
  });

  const createMutation = useMutation({
    mutationFn: (data: HomeworkCreate) => homeworkService.createHomework(data),
    onSuccess: (data) => {
      navigate(`/homework/${data.id}`);
    },
    onError: (error) => {
      console.error('Failed to create homework:', error);
      alert('Failed to create homework. Please try again.');
    },
  });

  const onSubmit = (data: HomeworkFormData) => {
    createMutation.mutate(data);
  };

  const selectedTextbook = watch('textbook_id');

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-5 h-5" />}
          onClick={() => navigate('/homework')}
        >
          Back
        </Button>
      </div>

      <div>
        <h1 className="text-3xl font-bold text-gray-900">Create Homework</h1>
        <p className="text-gray-600 mt-1">Create a new homework assignment for your class</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Basic Information</h2>
              </Card.Header>
              <Card.Body>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Title <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      {...register('title')}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                        errors.title ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Enter homework title"
                    />
                    {errors.title && (
                      <p className="text-red-500 text-sm mt-1">{errors.title.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Description
                    </label>
                    <textarea
                      {...register('description')}
                      rows={4}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      placeholder="Enter homework description and instructions"
                    />
                    {errors.description && (
                      <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Class <span className="text-red-500">*</span>
                      </label>
                      <select
                        {...register('class_id')}
                        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                          errors.class_id ? 'border-red-500' : 'border-gray-300'
                        }`}
                      >
                        <option value="">Select a class</option>
                        {classes.items.map((cls) => (
                          <option key={cls.id} value={cls.id}>
                            {cls.name}
                          </option>
                        ))}
                      </select>
                      {errors.class_id && (
                        <p className="text-red-500 text-sm mt-1">{errors.class_id.message}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Due Date <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="datetime-local"
                        {...register('due_date')}
                        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                          errors.due_date ? 'border-red-500' : 'border-gray-300'
                        }`}
                      />
                      {errors.due_date && (
                        <p className="text-red-500 text-sm mt-1">{errors.due_date.message}</p>
                      )}
                    </div>
                  </div>
                </div>
              </Card.Body>
            </Card>

            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Textbook Reference</h2>
              </Card.Header>
              <Card.Body>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Textbook
                    </label>
                    <select
                      {...register('textbook_id')}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    >
                      <option value="">None</option>
                      {textbooks.map((book: any) => (
                        <option key={book.id} value={book.id}>
                          {book.title}
                        </option>
                      ))}
                    </select>
                  </div>

                  {selectedTextbook && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Page Numbers
                      </label>
                      <input
                        type="text"
                        {...register('page_numbers')}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        placeholder="e.g., 45-50, 52"
                      />
                      <p className="text-sm text-gray-500 mt-1">
                        Enter page numbers or ranges (e.g., 45-50, 52, 60-65)
                      </p>
                    </div>
                  )}
                </div>
              </Card.Body>
            </Card>

            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Attachments</h2>
              </Card.Header>
              <Card.Body>
                <FileUpload
                  multiple
                  accept="image/*,application/pdf,.doc,.docx"
                  onFilesSelected={setAttachedFiles}
                  maxSize={10}
                />
                {attachedFiles.length > 0 && (
                  <p className="text-sm text-gray-600 mt-2">
                    {attachedFiles.length} file(s) selected
                  </p>
                )}
              </Card.Body>
            </Card>
          </div>

          <div className="space-y-6">
            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Actions</h2>
              </Card.Header>
              <Card.Body>
                <div className="space-y-3">
                  <Button
                    fullWidth
                    type="submit"
                    icon={<Send className="w-5 h-5" />}
                    loading={createMutation.isPending}
                    disabled={createMutation.isPending}
                  >
                    Assign Homework
                  </Button>
                  <Button
                    fullWidth
                    type="button"
                    variant="secondary"
                    icon={<Save className="w-5 h-5" />}
                    onClick={() => navigate('/homework')}
                  >
                    Cancel
                  </Button>
                </div>
              </Card.Body>
            </Card>

            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Tips</h2>
              </Card.Header>
              <Card.Body>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Provide clear instructions in the description</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Set a realistic due date</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Reference specific textbook pages if applicable</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Attach additional materials if needed</span>
                  </li>
                </ul>
              </Card.Body>
            </Card>
          </div>
        </div>
      </form>
    </div>
  );
};

export default CreateHomeworkPage;
