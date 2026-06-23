import { useRef } from 'react'
import { Link } from 'react-router-dom'
import {
  motion,
  useScroll,
  useTransform,
  useReducedMotion,
} from 'framer-motion'
import {
  ShieldCheck,
  ArrowRight,
  Layers,
  Sparkles,
  Gauge,
  FileCheck2,
  Users,
  Workflow,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'
import { Quote } from 'lucide-react'
import { Reveal, CountUp, useTilt } from '../components/motion'
import { LeadershipPreview, TeamLeadPreview, DevPreview } from '../components/PreviewCards'
import { orgScore, openOpenItems } from '../data/metrics'
import { controls } from '../data/controls'
import { personas, testimonial, teamFaces, type Persona } from '../data/people'

function Aurora() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="aurora animate-float-slow -left-32 -top-32 h-[36rem] w-[36rem]" style={{ background: 'radial-gradient(circle, #8b5cf6, transparent 70%)' }} />
      <div className="aurora animate-float-slower right-0 top-10 h-[32rem] w-[32rem]" style={{ background: 'radial-gradient(circle, #22d3ee, transparent 70%)' }} />
      <div className="aurora animate-float-slow bottom-0 left-1/3 h-[30rem] w-[30rem]" style={{ background: 'radial-gradient(circle, #10b981, transparent 70%)', animationDelay: '4s' }} />
    </div>
  )
}

function LandingNav() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 flex justify-center px-4 pt-4">
      <nav className="glass flex w-full max-w-5xl items-center justify-between rounded-2xl px-4 py-2.5">
        <Link to="/" className="flex items-center gap-2.5">
          <span className="grid h-8 w-8 place-items-center rounded-xl bg-iris text-white">
            <ShieldCheck className="h-4.5 w-4.5" />
          </span>
          <span className="font-display text-base font-semibold text-white">ComplyScope</span>
        </Link>
        <div className="hidden items-center gap-7 text-sm text-slate-300 md:flex">
          <a href="#platform" className="transition-colors hover:text-white">Platform</a>
          <a href="#features" className="transition-colors hover:text-white">Features</a>
          <a href="#stats" className="transition-colors hover:text-white">Impact</a>
        </div>
        <Link
          to="/app"
          className="group flex items-center gap-1.5 rounded-xl bg-white px-3.5 py-2 text-sm font-semibold text-ink-950 transition-transform duration-200 hover:scale-[1.03] cursor-pointer"
        >
          Launch platform
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
        </Link>
      </nav>
    </header>
  )
}

function Hero() {
  const ref = useRef<HTMLDivElement>(null)
  const reduce = useReducedMotion()
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] })
  const y = useTransform(scrollYProgress, [0, 1], [0, reduce ? 0 : 140])
  const scale = useTransform(scrollYProgress, [0, 1], [1, reduce ? 1 : 0.92])
  const opacity = useTransform(scrollYProgress, [0, 0.8], [1, reduce ? 1 : 0])

  return (
    <section ref={ref} className="relative flex min-h-screen flex-col items-center justify-center px-6 pb-24 pt-32">
      <Aurora />
      <motion.div style={{ y, opacity }} className="relative z-10 mx-auto max-w-4xl text-center">
        <motion.span
          initial={reduce ? false : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3.5 py-1.5 text-xs text-slate-300 backdrop-blur"
        >
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          Compliance posture, beautifully clear
        </motion.span>

        <motion.h1
          initial={reduce ? false : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.08, ease: [0.22, 1, 0.36, 1] }}
          className="mt-6 font-display text-5xl font-bold leading-[1.05] tracking-tight text-white sm:text-6xl md:text-7xl"
        >
          See exactly where
          <br />
          you stand on <span className="text-iris">compliance</span>
        </motion.h1>

        <motion.p
          initial={reduce ? false : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.18, ease: [0.22, 1, 0.36, 1] }}
          className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-slate-300/90"
        >
          One platform, layered for every role, leadership, team leads, and delivery teams.
          Understand your current state versus where you need to be, with AI summaries and
          audit readiness across every framework.
        </motion.p>

        <motion.div
          initial={reduce ? false : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.28, ease: [0.22, 1, 0.36, 1] }}
          className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row"
        >
          <Link
            to="/app"
            className="group flex items-center gap-2 rounded-2xl bg-white px-6 py-3.5 text-base font-semibold text-ink-950 transition-transform duration-200 hover:scale-[1.03] cursor-pointer"
          >
            Explore the platform
            <ArrowRight className="h-4.5 w-4.5 transition-transform group-hover:translate-x-1" />
          </Link>
          <a
            href="#platform"
            className="flex items-center gap-2 rounded-2xl border border-white/15 bg-white/5 px-6 py-3.5 text-base font-medium text-white backdrop-blur transition-colors duration-200 hover:bg-white/10 cursor-pointer"
          >
            How it works
          </a>
        </motion.div>
      </motion.div>

      {/* Floating layered preview */}
      <motion.div style={{ scale, opacity }} className="relative z-10 mt-16 w-full max-w-xl">
        <div className="absolute -inset-6 -z-10 rounded-[2rem] bg-iris opacity-20 blur-3xl" />
        <LeadershipPreview />
      </motion.div>

      <motion.a
        href="#problem"
        style={{ opacity }}
        className="absolute bottom-8 left-1/2 z-10 flex -translate-x-1/2 flex-col items-center gap-1 text-xs text-slate-400"
        aria-label="Scroll down"
      >
        Scroll
        <ChevronDown className="h-4 w-4 animate-bounce" />
      </motion.a>
    </section>
  )
}

function ProblemChapter() {
  return (
    <section id="problem" className="relative mx-auto max-w-4xl px-6 py-32 text-center">
      <Reveal>
        <p className="font-serif text-3xl font-medium leading-snug text-slate-400 sm:text-4xl md:text-5xl">
          Compliance data lives in
          <span className="text-slate-600"> spreadsheets, tickets, and inboxes.</span>{' '}
          <span className="text-white">Everyone sees a different version of the truth.</span>
        </p>
      </Reveal>
      <Reveal delay={0.15}>
        <p className="mx-auto mt-8 max-w-2xl text-lg text-slate-400">
          ComplyScope replaces that with a single, layered source of truth, where each
          person sees precisely the altitude they need.
        </p>
      </Reveal>
    </section>
  )
}

const layers = [
  {
    icon: Gauge,
    title: 'Leadership sees the headline',
    body: 'Org-wide posture, trend, audit readiness, and the few risks that actually matter, no noise.',
    preview: <LeadershipPreview />,
  },
  {
    icon: Users,
    title: 'Team leads see their pod',
    body: 'Where the team stands versus its target, which control areas lag, and what to close next.',
    preview: <TeamLeadPreview />,
  },
  {
    icon: Workflow,
    title: 'Delivery sees the work',
    body: 'Exactly what is being asked, why it matters, who owns it, and when it is due.',
    preview: <DevPreview />,
  },
]

function LayerCaption({ icon: Icon, title, body }: { icon: typeof Gauge; title: string; body: string }) {
  return (
    <div className="mt-5 text-center">
      <div className="flex items-center justify-center gap-2 text-iris">
        <Icon className="h-5 w-5" />
        <span className="font-display text-lg font-semibold text-white">{title}</span>
      </div>
      <p className="mx-auto mt-1.5 max-w-sm text-sm text-slate-400">{body}</p>
    </div>
  )
}

function LayeredSection() {
  const trackRef = useRef<HTMLDivElement>(null)
  const nudge = (dir: number) => {
    const el = trackRef.current
    if (!el) return
    const card = el.querySelector('[data-slide]') as HTMLElement | null
    const amount = card ? card.offsetWidth + 32 : Math.round(el.clientWidth * 0.85)
    el.scrollBy({ left: dir * amount, behavior: 'smooth' })
  }

  return (
    <section id="platform" className="mx-auto max-w-6xl px-6 py-24">
      <SectionHeading
        eyebrow="One platform, layered"
        title="Three views. One source of truth."
        sub="The same live data, at the right altitude for every role. Swipe to slide through each view."
      />
      <div className="relative mt-12">
        <div
          ref={trackRef}
          className="no-scrollbar -mx-6 flex snap-x snap-mandatory gap-8 overflow-x-auto scroll-smooth px-6 pb-4"
        >
          {layers.map((l) => (
            <div
              key={l.title}
              data-slide
              className="flex w-[82vw] shrink-0 snap-center flex-col sm:w-[24rem]"
            >
              {l.preview}
              <LayerCaption icon={l.icon} title={l.title} body={l.body} />
            </div>
          ))}
        </div>

        <button
          type="button"
          onClick={() => nudge(-1)}
          aria-label="Previous view"
          className="absolute -left-3 top-1/3 hidden h-11 w-11 place-items-center rounded-full border border-white/15 bg-white/10 text-white backdrop-blur transition hover:bg-white/20 md:grid"
        >
          <ChevronLeft className="h-5 w-5" />
        </button>
        <button
          type="button"
          onClick={() => nudge(1)}
          aria-label="Next view"
          className="absolute -right-3 top-1/3 hidden h-11 w-11 place-items-center rounded-full border border-white/15 bg-white/10 text-white backdrop-blur transition hover:bg-white/20 md:grid"
        >
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>
    </section>
  )
}

function TrustStrip() {
  return (
    <section className="mx-auto -mt-8 max-w-3xl px-6 pb-8">
      <Reveal className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
        <div className="flex -space-x-3">
          {teamFaces.map((src, i) => (
            <img
              key={i}
              src={src}
              alt=""
              aria-hidden
              loading="lazy"
              referrerPolicy="no-referrer"
              className="h-10 w-10 rounded-full border-2 border-ink-950 object-cover"
            />
          ))}
        </div>
        <p className="text-center text-sm text-slate-400 sm:text-left">
          Trusted by <span className="font-semibold text-white">leadership, security & delivery teams</span> to stay audit-ready.
        </p>
      </Reveal>
    </section>
  )
}

function PersonaCard({ persona, index }: { persona: Persona; index: number }) {
  const { rotateX, rotateY, onMove, onLeave } = useTilt(6)
  return (
    <Reveal delay={index * 0.1}>
      <motion.figure
        onMouseMove={onMove}
        onMouseLeave={onLeave}
        style={{ rotateX, rotateY, transformPerspective: 1000 }}
        className="card group relative h-full overflow-hidden p-6"
      >
        <div
          className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 rounded-full opacity-40 blur-2xl transition-opacity duration-300 group-hover:opacity-70"
          style={{ background: `radial-gradient(circle, ${persona.accent}, transparent 70%)` }}
        />
        <div className="relative flex items-center gap-4">
          <div className="rounded-full p-[2px]" style={{ background: `linear-gradient(135deg, ${persona.accent}, transparent)` }}>
            <img
              src={persona.photo}
              alt={`${persona.name}, ${persona.role}`}
              loading="lazy"
              referrerPolicy="no-referrer"
              className="h-16 w-16 rounded-full border-2 border-ink-900 object-cover"
            />
          </div>
          <figcaption>
            <div className="font-display text-lg font-semibold text-white">{persona.name}</div>
            <div className="text-sm" style={{ color: persona.accent }}>{persona.role}</div>
          </figcaption>
        </div>
        <Quote className="relative mt-5 h-6 w-6 text-white/20" />
        <blockquote className="relative mt-1 font-serif text-xl leading-snug text-slate-100">
          {persona.quote}
        </blockquote>
        <div className="relative mt-5 flex items-center gap-2 border-t border-white/8 pt-4 text-xs text-slate-400">
          <span className="font-semibold text-slate-300">They see:</span> {persona.sees}
        </div>
      </motion.figure>
    </Reveal>
  )
}

function PersonasSection() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-28">
      <SectionHeading
        eyebrow="The humans behind the layers"
        title="One platform. Three very different jobs."
        sub="Compliance touches everyone, so everyone gets a view built for how they actually work."
      />
      <div className="mt-14 grid gap-5 md:grid-cols-3">
        {personas.map((p, i) => (
          <PersonaCard key={p.name} persona={p} index={i} />
        ))}
      </div>
    </section>
  )
}

function TestimonialSection() {
  return (
    <section className="mx-auto max-w-5xl px-6 py-20">
      <Reveal>
        <figure className="glass-strong relative overflow-hidden rounded-3xl p-8 sm:p-12">
          <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-iris opacity-20 blur-3xl" />
          <Quote className="h-10 w-10 text-white/15" />
          <blockquote className="relative mt-2 font-serif text-2xl leading-snug text-white sm:text-3xl">
            “{testimonial.quote}”
          </blockquote>
          <figcaption className="relative mt-8 flex items-center gap-4">
            <img
              src={testimonial.photo}
              alt={`${testimonial.name}, ${testimonial.role}`}
              loading="lazy"
              referrerPolicy="no-referrer"
              className="h-14 w-14 rounded-full border-2 border-white/20 object-cover"
            />
            <div>
              <div className="font-display text-base font-semibold text-white">{testimonial.name}</div>
              <div className="text-sm text-slate-400">{testimonial.role}</div>
            </div>
          </figcaption>
        </figure>
      </Reveal>
    </section>
  )
}

function SectionHeading({ eyebrow, title, sub }: { eyebrow: string; title: string; sub?: string }) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      <Reveal>
        <span className="text-xs font-semibold uppercase tracking-widest text-iris">{eyebrow}</span>
      </Reveal>
      <Reveal delay={0.05}>
        <h2 className="mt-3 font-display text-4xl font-bold tracking-tight text-white sm:text-5xl">{title}</h2>
      </Reveal>
      {sub && (
        <Reveal delay={0.1}>
          <p className="mt-4 text-lg text-slate-400">{sub}</p>
        </Reveal>
      )}
    </div>
  )
}

interface Feature {
  icon: typeof Sparkles
  title: string
  body: string
  span: string
  tint: string
  visual?: React.ReactNode
}

const frameworkChips = ['SOC 2', 'ISO 27001', 'GDPR', 'HIPAA', 'PCI DSS']

const features: Feature[] = [
  {
    icon: Sparkles,
    title: 'AI summaries that read like a briefing',
    body: 'Every view opens with a short, generated narrative: what improved, what is at risk, and what to do next.',
    span: 'md:col-span-2 md:row-span-2',
    tint: 'from-violet-500/20',
    visual: (
      <div className="mt-5 rounded-xl border border-violet-400/20 bg-violet-500/10 p-4">
        <div className="flex items-center gap-2 text-xs font-medium text-violet-200">
          <Sparkles className="h-4 w-4" /> AI Executive Summary
        </div>
        <p className="mt-2 text-sm leading-relaxed text-slate-300">
          “Org posture is {orgScore}%, up 15 points over 12 months. Risk is concentrated in the
          payments CDE, with {openOpenItems.filter((o) => o.severity === 'critical').length} critical
          findings gating the autumn audits.”
        </p>
      </div>
    ),
  },
  {
    icon: Layers,
    title: 'Layered by role',
    body: 'Leadership, team-lead, and delivery views, same data, right altitude.',
    span: '',
    tint: 'from-cyan-500/20',
  },
  {
    icon: FileCheck2,
    title: 'Audit readiness',
    body: 'Readiness score, evidence freshness, and a live countdown to every assessment.',
    span: '',
    tint: 'from-emerald-500/20',
  },
  {
    icon: ShieldCheck,
    title: 'Five frameworks, one map',
    body: 'Controls unified across the standards that matter to you.',
    span: 'md:col-span-2',
    tint: 'from-indigo-500/20',
    visual: (
      <div className="mt-4 flex flex-wrap gap-2">
        {frameworkChips.map((f) => (
          <span key={f} className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-slate-200">
            {f}
          </span>
        ))}
      </div>
    ),
  },
]

function FeatureCard({ feature }: { feature: Feature }) {
  const { rotateX, rotateY, onMove, onLeave } = useTilt(5)
  return (
    <motion.div
      onMouseMove={onMove}
      onMouseLeave={onLeave}
      style={{ rotateX, rotateY, transformPerspective: 1000 }}
      className={`group card relative overflow-hidden p-6 ${feature.span}`}
    >
      <div className={`pointer-events-none absolute -right-16 -top-16 h-48 w-48 rounded-full bg-gradient-to-br ${feature.tint} to-transparent opacity-60 blur-2xl transition-opacity duration-300 group-hover:opacity-100`} />
      <div className="relative">
        <span className="grid h-11 w-11 place-items-center rounded-xl border border-white/10 bg-white/5 text-white">
          <feature.icon className="h-5 w-5" />
        </span>
        <h3 className="mt-4 font-display text-xl font-semibold text-white">{feature.title}</h3>
        <p className="mt-2 text-sm leading-relaxed text-slate-400">{feature.body}</p>
        {feature.visual}
      </div>
    </motion.div>
  )
}

function FeaturesSection() {
  return (
    <section id="features" className="mx-auto max-w-6xl px-6 py-28">
      <SectionHeading
        eyebrow="Everything in one place"
        title="Built for clarity, not dashboards"
        sub="Modular, glanceable, and honest about where you really are."
      />
      <div className="mt-14 grid gap-5 md:auto-rows-[1fr] md:grid-cols-3">
        {features.map((f) => (
          <Reveal key={f.title} className={f.span}>
            <FeatureCard feature={f} />
          </Reveal>
        ))}
      </div>
    </section>
  )
}

function StatsSection() {
  const stats = [
    { to: orgScore, suffix: '%', label: 'Current org posture' },
    { to: 5, suffix: '', label: 'Frameworks unified' },
    { to: controls.length, suffix: '', label: 'Controls tracked' },
    { to: 6, suffix: '', label: 'Delivery pods' },
  ]
  return (
    <section id="stats" className="relative mx-auto max-w-6xl px-6 py-24">
      <div className="glass-strong relative overflow-hidden rounded-3xl px-6 py-14">
        <div className="pointer-events-none absolute -left-20 -top-20 h-72 w-72 rounded-full bg-iris opacity-20 blur-3xl" />
        <div className="relative grid grid-cols-2 gap-10 text-center md:grid-cols-4">
          {stats.map((s) => (
            <div key={s.label}>
              <div className="font-display text-4xl font-bold text-white sm:text-5xl">
                <CountUp to={s.to} suffix={s.suffix} />
              </div>
              <div className="mt-2 text-sm text-slate-400">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function CTASection() {
  return (
    <section className="mx-auto max-w-5xl px-6 pb-32 pt-8">
      <div className="relative overflow-hidden rounded-[2rem] border border-white/10 p-12 text-center sm:p-16">
        <div className="absolute inset-0 -z-10 bg-iris opacity-90" />
        <div className="absolute inset-0 -z-10 grain opacity-30" />
        <Reveal>
          <h2 className="font-display text-4xl font-bold tracking-tight text-white sm:text-5xl">
            Ready to see your posture?
          </h2>
        </Reveal>
        <Reveal delay={0.1}>
          <p className="mx-auto mt-4 max-w-xl text-lg text-white/85">
            Open the live platform with realistic sample data across five frameworks and six pods.
          </p>
        </Reveal>
        <Reveal delay={0.2}>
          <Link
            to="/app"
            className="group mt-8 inline-flex items-center gap-2 rounded-2xl bg-white px-7 py-3.5 text-base font-semibold text-ink-950 transition-transform duration-200 hover:scale-[1.03] cursor-pointer"
          >
            Launch ComplyScope
            <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
          </Link>
        </Reveal>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="border-t border-white/10 px-6 py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 sm:flex-row">
        <div className="flex items-center gap-2.5">
          <span className="grid h-7 w-7 place-items-center rounded-lg bg-iris text-white">
            <ShieldCheck className="h-4 w-4" />
          </span>
          <span className="font-display font-semibold text-white">ComplyScope</span>
        </div>
        <p className="text-xs text-slate-500">Demo experience · Sample data · Built for stakeholder presentations</p>
      </div>
    </footer>
  )
}

export default function Landing() {
  return (
    <div className="relative bg-ink-950">
      <LandingNav />
      <Hero />
      <TrustStrip />
      <ProblemChapter />
      <LayeredSection />
      <PersonasSection />
      <FeaturesSection />
      <TestimonialSection />
      <StatsSection />
      <CTASection />
      <Footer />
    </div>
  )
}
