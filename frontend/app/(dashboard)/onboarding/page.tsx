"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { userApi, topicsApi } from "@/lib/api";
import { useQuery, useMutation } from "@tanstack/react-query";
import {
  Loader2,
  Upload,
  FileText,
  Check,
  ChevronRight,
  ChevronLeft,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [skillAnalysis, setSkillAnalysis] = useState<any>(null);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [duration, setDuration] = useState(30);

  // Fetch topics
  const { data: topics, isLoading: topicsLoading } = useQuery({
    queryKey: ["topics"],
    queryFn: async () => {
      const response = await topicsApi.getAll();
      return response.data;
    },
  });

  // Resume upload mutation
  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const response = await userApi.uploadResume(file);
      return response.data;
    },
    onSuccess: (data) => {
      setSkillAnalysis(data);
      setStep(2);
    },
  });

  // Topic selection mutation
  const selectTopicsMutation = useMutation({
    mutationFn: async () => {
      const response = await topicsApi.select({
        topic_ids: selectedTopics,
        duration_days: duration,
      });
      return response.data;
    },
    onSuccess: () => {
      router.push("/dashboard");
    },
  });

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setResumeFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        [".docx"],
    },
    maxFiles: 1,
    maxSize: 5 * 1024 * 1024, // 5MB
  });

  const handleUploadResume = () => {
    if (resumeFile) {
      uploadMutation.mutate(resumeFile);
    }
  };

  const toggleTopic = (topicId: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topicId)
        ? prev.filter((id) => id !== topicId)
        : [...prev, topicId]
    );
  };

  const handleComplete = () => {
    if (selectedTopics.length > 0) {
      selectTopicsMutation.mutate();
    }
  };

  const skipResume = () => {
    setStep(2);
  };

  return (
    <div className="min-h-screen bg-muted/50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress indicator */}
        <div className="mb-8">
          <div className="flex justify-between text-sm text-muted-foreground mb-2">
            <span>Step {step} of 2</span>
            <span>{step === 1 ? "Resume Analysis" : "Select Topics"}</span>
          </div>
          <Progress value={step * 50} className="h-2" />
        </div>

        {/* Step 1: Resume Upload */}
        {step === 1 && (
          <Card>
            <CardHeader>
              <CardTitle>Upload Your Resume</CardTitle>
              <CardDescription>
                We&apos;ll analyze your skills to create a personalized learning
                path. This step is optional.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div
                {...getRootProps()}
                className={cn(
                  "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
                  isDragActive
                    ? "border-primary bg-primary/5"
                    : "border-muted-foreground/25 hover:border-primary/50"
                )}
              >
                <input {...getInputProps()} />
                {resumeFile ? (
                  <div className="flex items-center justify-center space-x-3">
                    <FileText className="h-8 w-8 text-primary" />
                    <div className="text-left">
                      <p className="font-medium">{resumeFile.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {(resumeFile.size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Upload className="h-10 w-10 mx-auto text-muted-foreground" />
                    <p className="text-muted-foreground">
                      Drag & drop your resume here, or click to select
                    </p>
                    <p className="text-xs text-muted-foreground">
                      PDF or DOCX, max 5MB
                    </p>
                  </div>
                )}
              </div>

              <div className="flex justify-between">
                <Button variant="ghost" onClick={skipResume}>
                  Skip for now
                </Button>
                <Button
                  onClick={handleUploadResume}
                  disabled={!resumeFile || uploadMutation.isPending}
                >
                  {uploadMutation.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      Analyze Resume
                      <ChevronRight className="ml-2 h-4 w-4" />
                    </>
                  )}
                </Button>
              </div>

              {uploadMutation.isError && (
                <p className="text-sm text-red-500">
                  Failed to analyze resume. Please try again.
                </p>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step 2: Topic Selection */}
        {step === 2 && (
          <Card>
            <CardHeader>
              <CardTitle>Choose Your Topics</CardTitle>
              <CardDescription>
                Select one or more topics to master. We&apos;ll create a
                personalized roadmap for you.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Skill Analysis Results */}
              {skillAnalysis && (
                <div className="p-4 bg-primary/5 rounded-lg mb-4">
                  <h4 className="font-medium mb-2">Your Skill Analysis</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">Level:</span>{" "}
                      <span className="capitalize">
                        {skillAnalysis.experience_level}
                      </span>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Skills:</span>{" "}
                      {skillAnalysis.skills?.slice(0, 3).join(", ")}
                    </div>
                  </div>
                  {skillAnalysis.recommended_topics?.length > 0 && (
                    <p className="text-sm mt-2">
                      <span className="text-muted-foreground">Recommended:</span>{" "}
                      {skillAnalysis.recommended_topics.join(", ")}
                    </p>
                  )}
                </div>
              )}

              {/* Topic Grid */}
              {topicsLoading ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-3">
                  {topics?.map((topic: any) => (
                    <button
                      key={topic.id}
                      onClick={() => toggleTopic(topic.id)}
                      className={cn(
                        "p-4 rounded-lg border text-left transition-all",
                        selectedTopics.includes(topic.id)
                          ? "border-primary bg-primary/5"
                          : "border-border hover:border-primary/50"
                      )}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <span className="text-xl mr-2">{topic.icon}</span>
                          <span className="font-medium">{topic.name}</span>
                        </div>
                        {selectedTopics.includes(topic.id) && (
                          <Check className="h-5 w-5 text-primary" />
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        {topic.total_concepts} concepts
                      </p>
                    </button>
                  ))}
                </div>
              )}

              {/* Duration Selection */}
              <div className="space-y-3">
                <label className="text-sm font-medium">Learning Duration</label>
                <div className="flex gap-3">
                  {[30, 60, 90].map((days) => (
                    <button
                      key={days}
                      onClick={() => setDuration(days)}
                      className={cn(
                        "flex-1 py-2 px-4 rounded-md border text-sm font-medium transition-colors",
                        duration === days
                          ? "border-primary bg-primary text-primary-foreground"
                          : "border-border hover:border-primary/50"
                      )}
                    >
                      {days} Days
                    </button>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-between pt-4">
                <Button variant="ghost" onClick={() => setStep(1)}>
                  <ChevronLeft className="mr-2 h-4 w-4" />
                  Back
                </Button>
                <Button
                  onClick={handleComplete}
                  disabled={
                    selectedTopics.length === 0 || selectTopicsMutation.isPending
                  }
                >
                  {selectTopicsMutation.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Creating roadmap...
                    </>
                  ) : (
                    <>
                      Start Learning
                      <ChevronRight className="ml-2 h-4 w-4" />
                    </>
                  )}
                </Button>
              </div>

              {selectTopicsMutation.isError && (
                <p className="text-sm text-red-500">
                  Failed to create roadmap. Please try again.
                </p>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
