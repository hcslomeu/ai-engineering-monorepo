# ---- Stage 1: Dependencies ----
FROM node:22-slim AS deps

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable && corepack prepare pnpm@10.28.1 --activate

WORKDIR /app

# Copy dependency manifests first (cache-friendly layer ordering)
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
# Future: uncomment as workspace packages are created
# COPY apps/alpha-whale/web/package.json apps/alpha-whale/web/
# COPY libs/shared-schemas/package.json libs/shared-schemas/

RUN --mount=type=cache,target=/pnpm/store \
    pnpm install --frozen-lockfile


# ---- Stage 2: Builder ----
FROM deps AS builder

WORKDIR /app

# Copy source code (specific directories, not COPY . . which leaks .env)
COPY nx.json tsconfig.base.json tsconfig.json ./
COPY libs/ libs/
COPY apps/ apps/

# Future: build the Next.js app (requires WP-004)
# RUN pnpm nx build alpha-whale-web


# ---- Stage 3: Runtime ----
FROM node:22-slim AS runtime

ENV NODE_ENV=production

WORKDIR /app

# Future: copy Next.js standalone output with correct ownership (requires WP-004)
# COPY --chown=node:node --from=builder /app/apps/alpha-whale/web/.next/standalone ./
# COPY --chown=node:node --from=builder /app/apps/alpha-whale/web/.next/static ./.next/static
# COPY --chown=node:node --from=builder /app/apps/alpha-whale/web/public ./public

USER node

EXPOSE 3000

# Future: start the Next.js standalone server
# CMD ["node", "server.js"]
CMD ["node", "--version"]
