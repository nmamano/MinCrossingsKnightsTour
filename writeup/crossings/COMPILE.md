# Crossings post: MDX check

2026-10-02. Run from the research project root:

```sh
node writeup/crossings/check_mdx.mjs
```

PASS on 2026-10-02. The output is in `writeup/crossings/compile.log`.
The script reads the installed compiler packages from
`/home/nil/nil/nilmamano.com/node_modules`. It strips frontmatter with
`gray-matter`, as the site's `app/lib/blog.ts` does, and calls the
`next-mdx-remote` serializer in RSC mode. The options match
`app/blog/[slug]/page.tsx`: `blockJS: false`, `remarkPlugins: [remarkGfm]`,
and `rehypePlugins: []`. The site's RSC compiler uses that serializer.
The script verifies that there are two closed appendix details blocks
and neither has an `open` attribute.

No site file is changed. This is a compilation check, not a site build or
a deployment. The research post is the only MDX input.
