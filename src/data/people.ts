/** People used in the marketing storytelling. Portraits are stable, free
 *  headshots from randomuser.me (clearly photos of people, no licensing fuss). */

export interface Persona {
  name: string
  role: string
  photo: string
  quote: string
  sees: string
  accent: string
}

export const personas: Persona[] = [
  {
    name: 'Alex Carter',
    role: 'VP, Security & Compliance',
    photo: 'https://randomuser.me/api/portraits/men/32.jpg',
    quote: 'I walk into the board meeting knowing our number and the three risks behind it.',
    sees: 'The headline: posture, trend, audit readiness.',
    accent: '#a78bfa',
  },
  {
    name: 'Priya Nair',
    role: 'Payments Team Lead',
    photo: 'https://randomuser.me/api/portraits/women/65.jpg',
    quote: 'I can finally see where my pod stands versus target, and exactly what to close next.',
    sees: 'Her pod: gaps, targets, owned controls.',
    accent: '#22d3ee',
  },
  {
    name: 'Marcus Lee',
    role: 'Platform PM',
    photo: 'https://randomuser.me/api/portraits/men/75.jpg',
    quote: 'Every task tells me what is being asked, why it matters, and when it is due.',
    sees: 'The work: tickets, owners, due dates.',
    accent: '#34d399',
  },
]

export interface Testimonial {
  name: string
  role: string
  photo: string
  quote: string
}

export const testimonial: Testimonial = {
  name: 'Dr. Aisha Khan',
  role: 'Head of Clinical Products',
  photo: 'https://randomuser.me/api/portraits/women/72.jpg',
  quote:
    'For the first time, leadership, my team leads, and our engineers are all looking at the same truth, just at the altitude each of them needs. Audit prep went from weeks to an afternoon.',
}

/** Faces for the "trusted by teams" strip. */
export const teamFaces: string[] = [
  'https://randomuser.me/api/portraits/women/44.jpg',
  'https://randomuser.me/api/portraits/men/46.jpg',
  'https://randomuser.me/api/portraits/women/12.jpg',
  'https://randomuser.me/api/portraits/men/22.jpg',
  'https://randomuser.me/api/portraits/women/90.jpg',
  'https://randomuser.me/api/portraits/men/60.jpg',
]
