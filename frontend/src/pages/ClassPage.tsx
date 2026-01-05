import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Layout } from '../components/Layout';
import { api } from '../services/api';
import { Class, File, ChatResponse } from '../types';

export function ClassPage() {
  const { classId } = useParams<{ classId: string }>();
  const [class_, setClass] = useState<Class | null>(null);
  const [files, setFiles] = useState<File[]>([]);
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string; sources?: any[] }>>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (classId) {
      loadClassData();
    }
  }, [classId]);

  const loadClassData = async () => {
    try {
      const [classData, filesData] = await Promise.all([
        api.getClass(Number(classId)),
        api.getFiles(Number(classId)),
      ]);
      setClass(classData);
      setFiles(filesData);
    } catch (error) {
      console.error('Failed to load class data', error);
      navigate('/');
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !classId) return;

    setIsLoading(true);
    setUploadProgress(0);

    try {
      await api.uploadFile(Number(classId), file, (progress) => {
        setUploadProgress(progress);
      });
      await loadClassData();
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      console.error('Failed to upload file', error);
      alert('Failed to upload file');
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  };

  const handleDeleteFile = async (fileId: number) => {
    if (!confirm('Are you sure you want to delete this file?')) return;

    try {
      await api.deleteFile(fileId);
      await loadClassData();
    } catch (error) {
      console.error('Failed to delete file', error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || !classId || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await api.chat({
        class_id: Number(classId),
        message: userMessage,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.answer,
          sources: response.sources,
        },
      ]);
    } catch (error) {
      console.error('Failed to send message', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error processing your question.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    const mb = bytes / (1024 * 1024);
    return mb < 1 ? `${(bytes / 1024).toFixed(1)} KB` : `${mb.toFixed(1)} MB`;
  };

  if (!class_) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="text-gray-500">Loading...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 hover:text-blue-800 mb-2"
          >
            ← Back to Classes
          </button>
          <h2 className="text-2xl font-bold text-gray-900">{class_.name}</h2>
          {class_.description && (
            <p className="text-gray-600 mt-1">{class_.description}</p>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Files Section */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-4">Files</h3>

            <div className="mb-4">
              <label className="flex items-center justify-center w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 cursor-pointer">
                <span>Upload File (Audio/PDF)</span>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".mp3,.wav,.m4a,.ogg,.flac,.aac,.wma,.pdf"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
              {uploadProgress > 0 && (
                <div className="mt-2">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    {uploadProgress < 100 ? `Uploading... ${uploadProgress}%` : 'Processing audio (this may take several minutes)...'}
                  </p>
                </div>
              )}
            </div>

            <div className="space-y-2 max-h-96 overflow-y-auto">
              {files.length === 0 ? (
                <p className="text-gray-500 text-sm">No files uploaded yet</p>
              ) : (
                files.map((file) => (
                  <div
                    key={file.id}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {file.original_filename}
                      </p>
                      <p className="text-xs text-gray-500">
                        {file.file_type} • {formatFileSize(file.file_size)} •{' '}
                        {file.is_processed ? '✓ Processed' : '⏳ Processing...'}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDeleteFile(file.id)}
                      className="ml-2 text-red-600 hover:text-red-800 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Chat Section */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 flex flex-col">
            <h3 className="text-lg font-semibold mb-4">Ask Questions</h3>

            <div className="flex-1 overflow-y-auto space-y-4 mb-4 max-h-96">
              {messages.length === 0 ? (
                <p className="text-gray-500 text-sm">
                  Upload files and start asking questions about your class materials!
                </p>
              ) : (
                messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-lg ${
                      msg.role === 'user'
                        ? 'bg-blue-100 ml-12'
                        : 'bg-gray-100 mr-12'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-2 text-xs text-gray-600">
                        <p className="font-semibold">Sources:</p>
                        {msg.sources.map((src, i) => (
                          <p key={i}>• {src.filename}</p>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
              {isLoading && (
                <div className="bg-gray-100 p-3 rounded-lg mr-12">
                  <p className="text-sm text-gray-500">Thinking...</p>
                </div>
              )}
            </div>

            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask a question..."
                disabled={isLoading || files.length === 0}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
              />
              <button
                type="submit"
                disabled={isLoading || !inputMessage.trim() || files.length === 0}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
}
