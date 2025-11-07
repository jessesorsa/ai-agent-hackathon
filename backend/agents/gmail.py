"""Gmail Agent for drafting personalized sales emails."""
from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, SystemMessage

from agents.base import BaseAgent
from core.config import Config


class GmailAgent(BaseAgent):
    """
    Gmail Agent for drafting personalized sales emails.
    
    Features:
    - Context-aware personalization using HubSpot CRM data
    - Tone adaptation based on sales stage
    - Email templates for different scenarios
    """
    
    def __init__(self):
        """Initialize the Gmail Agent."""
        super().__init__("Gmail Agent")
        try:
            self.llm = Config.get_llm()
            self._email_templates = self._load_email_templates()
            self.log_info("Gmail Agent initialized successfully")
        except Exception as e:
            self.log_error(f"Failed to initialize Gmail Agent: {str(e)}")
            raise
    
    def _load_email_templates(self) -> Dict[str, str]:
        """
        Load email templates for different scenarios.
        
        Returns:
            Dict mapping email type to template guidance
        """
        return {
            "initial_outreach": """
You are drafting an initial outreach email to a potential customer. 
Keep it concise, value-focused, and personalized based on their company context.
Focus on their pain points and how your solution can help.
""",
            "follow_up": """
You are drafting a follow-up email. Reference previous interactions naturally.
Be helpful and non-pushy. Show you remember the conversation.
Provide value or answer questions from previous exchanges.
""",
            "demo_scheduled": """
You are drafting a pre-demo email. Confirm details, set expectations, and build excitement.
Make it clear what they'll see and how it will help them.
""",
            "post_demo": """
You are drafting a post-demo follow-up. Thank them, summarize key points discussed,
and provide next steps or answer questions. Be helpful and address any concerns.
""",
            "closing": """
You are drafting a closing email. Be direct but respectful. Address any final concerns
and make it easy for them to say yes. Remove friction and provide clear next steps.
"""
        }
    
    def _get_tone_guidance(self, sales_stage: Optional[str] = None, 
                          email_type: Optional[str] = None,
                          relationship_history: Optional[Dict] = None) -> str:
        """
        Get tone guidance based on sales stage and context.
        
        Args:
            sales_stage: Current sales stage from CRM
            email_type: Type of email being drafted
            relationship_history: History of interactions
        
        Returns:
            String with tone guidance for the LLM
        """
        # Base tone map by sales stage
        tone_map = {
            "lead": "Professional but warm. Focus on value proposition and building initial rapport.",
            "qualified": "More conversational. Build rapport while demonstrating expertise.",
            "demo_scheduled": "Enthusiastic and helpful. Set clear expectations and build excitement.",
            "negotiation": "Direct and solution-focused. Address concerns proactively.",
            "closing": "Confident and supportive. Remove friction and make decision easy."
        }
        
        # Default tone
        default_tone = "Professional, friendly, and value-focused."
        
        # Determine base tone from sales stage
        base_tone = tone_map.get(sales_stage.lower(), default_tone) if sales_stage else default_tone
        
        # Adjust based on relationship history
        if relationship_history:
            interaction_count = relationship_history.get("interaction_count", 0)
            if interaction_count == 0:
                # First contact - more formal
                base_tone += " This is the first contact, so maintain a professional tone."
            elif interaction_count > 3:
                # Established relationship - more casual
                base_tone += " You have an established relationship, so you can be more casual and friendly."
        
        # Adjust based on email type
        if email_type == "initial_outreach":
            base_tone += " Keep it concise and avoid being too salesy."
        elif email_type == "follow_up":
            base_tone += " Reference previous conversations naturally and show continuity."
        
        return base_tone
    
    def _build_email_context(self, 
                            recipient: str,
                            contact_info: Optional[Dict] = None,
                            company_info: Optional[Dict] = None,
                            crm_context: Optional[Dict] = None) -> str:
        """
        Build context string for email personalization.
        
        Args:
            recipient: Email address of recipient
            contact_info: Contact information from CRM
            company_info: Company information from research
            crm_context: Additional CRM context (deal stage, notes, etc.)
        
        Returns:
            Formatted context string for the LLM
        """
        context_parts = []
        
        # Contact information
        if contact_info:
            context_parts.append("=== CONTACT INFORMATION ===")
            context_parts.append(f"Name: {contact_info.get('name', 'Unknown')}")
            if contact_info.get('title'):
                context_parts.append(f"Title: {contact_info['title']}")
            if contact_info.get('last_contact'):
                context_parts.append(f"Last contacted: {contact_info['last_contact']}")
            if contact_info.get('previous_interactions'):
                context_parts.append(f"Previous interactions: {contact_info['previous_interactions']}")
        
        # Company information
        if company_info:
            context_parts.append("\n=== COMPANY INFORMATION ===")
            context_parts.append(f"Company: {company_info.get('name', 'Unknown')}")
            if company_info.get('industry'):
                context_parts.append(f"Industry: {company_info['industry']}")
            if company_info.get('size'):
                context_parts.append(f"Company size: {company_info['size']}")
            if company_info.get('recent_news'):
                context_parts.append(f"Recent news: {company_info['recent_news']}")
            if company_info.get('tech_stack'):
                context_parts.append(f"Tech stack: {company_info['tech_stack']}")
        
        # CRM context
        if crm_context:
            context_parts.append("\n=== CRM CONTEXT ===")
            if crm_context.get('deal_stage'):
                context_parts.append(f"Deal stage: {crm_context['deal_stage']}")
            if crm_context.get('deal_amount'):
                context_parts.append(f"Deal amount: {crm_context['deal_amount']}")
            if crm_context.get('last_meeting_notes'):
                context_parts.append(f"Last meeting notes: {crm_context['last_meeting_notes']}")
            if crm_context.get('previous_interactions'):
                context_parts.append(f"Previous interactions: {crm_context['previous_interactions']}")
            if crm_context.get('pain_points'):
                context_parts.append(f"Identified pain points: {crm_context['pain_points']}")
            if crm_context.get('next_steps'):
                context_parts.append(f"Planned next steps: {crm_context['next_steps']}")
        
        return "\n".join(context_parts) if context_parts else "No additional context available."
    
    def _infer_email_type(self, intent: str, crm_context: Optional[Dict] = None) -> str:
        """
        Infer email type from intent and CRM context.
        
        Args:
            intent: User's intent for the email
            crm_context: CRM context that might indicate email type
        
        Returns:
            Email type string (initial_outreach, follow_up, demo_scheduled, post_demo, closing)
        """
        intent_lower = intent.lower()
        
        # Check for explicit email type keywords
        if any(word in intent_lower for word in ["initial", "first", "outreach", "cold", "introduction"]):
            return "initial_outreach"
        elif any(word in intent_lower for word in ["demo", "demonstration"]):
            if any(word in intent_lower for word in ["scheduled", "upcoming", "pre-", "before"]):
                return "demo_scheduled"
            elif any(word in intent_lower for word in ["after", "post", "following"]):
                return "post_demo"
            else:
                return "post_demo"  # Default demo-related to post_demo
        elif any(word in intent_lower for word in ["follow", "follow-up", "followup", "checking in"]):
            return "follow_up"
        elif any(word in intent_lower for word in ["close", "closing", "final", "decision"]):
            return "closing"
        
        # Infer from CRM context if intent is ambiguous
        if crm_context:
            deal_stage = crm_context.get("deal_stage", "").lower()
            if "demo" in deal_stage and "scheduled" in deal_stage:
                return "demo_scheduled"
            elif "demo" in deal_stage:
                return "post_demo"
            elif any(stage in deal_stage for stage in ["qualified", "lead"]):
                return "follow_up"
            elif "closing" in deal_stage or "negotiation" in deal_stage:
                return "closing"
        
        # Default to follow_up if we can't determine
        return "follow_up"
    
    def _parse_email_response(self, response: str) -> tuple[str, str]:
        """
        Parse LLM response to extract subject and body.
        
        Args:
            response: Raw response from LLM
        
        Returns:
            Tuple of (subject, body)
        """
        lines = response.strip().split('\n')
        subject = ""
        body_lines = []
        in_body = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # Look for explicit SUBJECT: tag
            if line_stripped.upper().startswith("SUBJECT:"):
                subject = line_stripped.split(":", 1)[1].strip()
            # Look for explicit BODY: tag
            elif line_stripped.upper().startswith("BODY:"):
                in_body = True
            # If we're in body section, collect lines
            elif in_body:
                body_lines.append(line)
            # If no explicit tags and we don't have a subject yet, first short line might be subject
            elif not subject and not in_body and len(line_stripped) < 100 and line_stripped:
                # Check if it looks like a subject (not too long, ends with punctuation or is short)
                if len(line_stripped) <= 80:
                    subject = line_stripped
                    in_body = True
                else:
                    # Too long to be subject, must be body
                    body_lines.append(line)
                    in_body = True
            # Otherwise, it's part of the body
            else:
                body_lines.append(line)
                if not in_body:
                    in_body = True
        
        body = '\n'.join(body_lines).strip()
        
        # Fallback if parsing fails
        if not subject:
            # Try to extract first line as subject if it's short
            first_line = response.strip().split('\n')[0] if response.strip() else ""
            if len(first_line) <= 100:
                subject = first_line
                body = '\n'.join(response.strip().split('\n')[1:]).strip()
            else:
                subject = "Following up"  # Default subject
        
        if not body:
            # If we couldn't parse body, use the whole response
            body = response.strip()
        
        return subject, body
    
    async def draft_email(
        self,
        recipient: str,
        intent: str,
        contact_info: Optional[Dict] = None,
        company_info: Optional[Dict] = None,
        crm_context: Optional[Dict] = None,
        email_type: Optional[str] = None,
        custom_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Draft a personalized email.
        
        Args:
            recipient: Email address of recipient
            intent: User's intent for the email (e.g., "follow-up", "initial outreach")
            contact_info: Contact information from CRM
            company_info: Company information from research
            crm_context: Additional CRM context (deal stage, notes, etc.)
            email_type: Type of email (initial_outreach, follow_up, demo_scheduled, etc.)
                       If not provided, will be inferred from intent and context
            custom_instructions: Any custom instructions for the email
        
        Returns:
            Dict with 'subject', 'body', 'context_used', 'reasoning', and 'success'
        """
        try:
            self.log_info(f"Drafting email to {recipient}", {"intent": intent})
            
            # Determine email type if not provided
            if not email_type:
                email_type = self._infer_email_type(intent, crm_context)
                self.log_info(f"Inferred email type: {email_type}")
            
            # Get template and tone guidance
            template_guidance = self._email_templates.get(
                email_type, 
                self._email_templates["follow_up"]
            )
            
            sales_stage = crm_context.get("deal_stage") if crm_context else None
            relationship_history = {
                "interaction_count": contact_info.get("interaction_count", 0) if contact_info else 0
            }
            
            tone_guidance = self._get_tone_guidance(
                sales_stage=sales_stage,
                email_type=email_type,
                relationship_history=relationship_history if relationship_history["interaction_count"] > 0 else None
            )
            
            # Build context string
            context_str = self._build_email_context(
                recipient, contact_info, company_info, crm_context
            )
            
            # Build system prompt
            system_prompt = f"""You are an expert sales email writer. Your task is to draft personalized, 
effective sales emails that drive engagement and build relationships.

{template_guidance}

Tone guidelines: {tone_guidance}

Key principles:
- Be concise (3-4 short paragraphs max)
- Personalize based on context provided
- Focus on value, not features
- Include a clear call-to-action
- Sound human, not robotic
- Use the recipient's name naturally (if provided)
- Avoid generic phrases and clichés
- Make it easy to respond
"""
            
            # Build human prompt
            human_prompt = f"""Draft an email with the following context:

Recipient: {recipient}
User Intent: {intent}

Context:
{context_str}

{f'Custom Instructions: {custom_instructions}' if custom_instructions else ''}

Please provide:
1. A compelling subject line (max 60 characters)
2. The email body (professional but personable, 3-4 paragraphs)

Format your response as:
SUBJECT: [subject line]
BODY:
[email body]
"""
            
            # Generate email using LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            self.log_info("Calling LLM to generate email")
            response = await self.llm.ainvoke(messages)
            email_content = response.content
            
            # Parse response
            subject, body = self._parse_email_response(email_content)
            
            # Track what context was used
            context_used = {
                "contact_info": bool(contact_info),
                "company_info": bool(company_info),
                "crm_context": bool(crm_context),
                "email_type": email_type,
                "sales_stage": sales_stage,
                "tone_guidance": tone_guidance
            }
            
            self.log_info(f"Successfully drafted email: {subject[:50]}...")
            
            return {
                "success": True,
                "recipient": recipient,
                "subject": subject,
                "body": body,
                "context_used": context_used,
                "reasoning": f"Drafted {email_type} email using {tone_guidance[:50]}... tone",
                "agent": self.name
            }
            
        except Exception as e:
            return self.handle_error(e, {
                "recipient": recipient,
                "intent": intent,
                "email_type": email_type
            })
    
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute method for BaseAgent interface.
        
        This method delegates to draft_email() for compatibility with the base agent interface.
        All arguments are passed through to draft_email().
        
        Returns:
            Dict with execution results
        """
        return await self.draft_email(*args, **kwargs)
