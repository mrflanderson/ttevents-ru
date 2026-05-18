import { defineCollection, z } from "astro/config";

export const collections = {
  blog: defineCollection({
    schema: z.object({
      title: z.string(),
      description: z.string(),
      date: z.string().transform((val) => new Date(val)),
      published: z.boolean().default(true),
      coverImage: z.string(),
      tags: z.array(z.string()),
    }),
  }),
  cases: defineCollection({
    schema: z.object({
      title: z.string(),
      description: z.string(),
      date: z
        .string()
        .transform((val) => new Date(val))
        .optional(),
      published: z.boolean().default(true),
      coverImage: z.string(),
      tags: z.array(z.string()).default([]),
      client: z.string().optional(),
      budget: z.string().optional(),
    }),
  }),
  services: defineCollection({
    schema: z.object({
      title: z.string(),
      description: z.string(),
      icon: z.enum([
        "briefcase",
        "team",
        "tree",
        "building",
        "rocket",
        "camera",
      ]),
      relatedLinks: z.array(z.string()).optional(),
    }),
  }),
};
