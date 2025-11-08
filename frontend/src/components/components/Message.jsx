'use client'

import { Button } from "@/components/ui/button"
import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {
    Building2,
    Briefcase,
    Target,
    Globe,
    MapPin,
    Users,
    DollarSign,
    FileText,
    ExternalLink,
    Eye,
    Plus,
    Calendar,
    Clock,
    Mail,
    MessageSquare,
    Info
} from "lucide-react"
import ReactMarkdown from "react-markdown";
import 'github-markdown-css/github-markdown.css'

// Default test company data
const DEFAULT_COMPANY_DATA = {
    name: "Acme Corporation",
    industry: "Software and Technology",
    icpFit: 85,
    domain: "acme.com",
    website: "https://acme.com",
    location: "San Francisco, CA",
    employeeCount: "50-100",
    revenue: "$5M - $10M",
    description: "Acme Corporation is a leading provider of enterprise software solutions, specializing in cloud-based infrastructure and AI-powered analytics. Founded in 2015, we help businesses transform their digital operations through innovative technology."
};

// Default test event data
const DEFAULT_EVENT_DATA = {
    title: "Meeting Scheduled",
    description: "Team sync meeting with Acme Corporation",
    timestamp: "2:00 PM - 3:00 PM",
    location: "Conference Room A"
};



/**
 * Message component that displays a single message
 * @param {Object} props
 * @param {string} props.role - 'user' or 'agent' or 'company' or 'event'
 * @param {string|Object} props.content - The message content
 * @param {string} props.className - Additional CSS classes
 */
const Message = ({ role, content, className }) => {

    if (role === 'user') {
        return (
            <div className="flex justify-start">
                <Card
                    className="p-3 w-fit shadow-none border-none bg-neutral-100">
                    <CardContent
                        className="p-0">
                        {content}
                    </CardContent>
                </Card >
            </div>
        );
    }

    if (role === 'table') {
        // Parse table data from content
        let tableData;
        if (!content) {
            tableData = DEFAULT_TABLE_DATA;
        } else if (typeof content === 'string') {
            try {
                tableData = JSON.parse(content);
            } catch (e) {
                tableData = DEFAULT_TABLE_DATA;
            }
        } else {
            tableData = content;
        }

        const { columns = [], data = [] } = tableData;

        return (
            <div className="flex justify-center w-full my-6">
                <Card className="w-full max-w-4xl p-12">
                    <CardContent className="p-4">
                        <div className="overflow-x-auto rounded-md border">
                            <table className="w-full">
                                <thead>
                                    <tr className="border-b">
                                        {columns.map((column, index) => (
                                            <th key={index} className="h-12 px-4 text-left align-middle font-medium text-xs text-muted-foreground">
                                                {column.header || column.key}
                                            </th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.length > 0 ? (
                                        data.map((row, rowIndex) => (
                                            <tr key={rowIndex} className="border-b text-md">
                                                {columns.map((column, colIndex) => (
                                                    <td key={colIndex} className="p-4 align-middle">
                                                        {row[column.key] || ''}
                                                    </td>
                                                ))}
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td
                                                colSpan={columns.length}
                                                className="h-24 text-center p-4 text-muted-foreground"
                                            >
                                                No data.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    if (role === 'company') {

        // Parse company data from content
        let companyData;
        if (!content) {
            companyData = DEFAULT_COMPANY_DATA;
        } else if (typeof content === 'string') {
            try {
                companyData = JSON.parse(content);
            } catch (e) {
                companyData = DEFAULT_COMPANY_DATA;
            }
        } else {
            companyData = content;
        }

        const { name, industry, icpFit, domain, website, location, employeeCount, revenue, description } = companyData;

        return (
            <div className="flex justify-center w-full my-6">
                <Card className="w-full max-w-md">
                    <CardHeader>
                        <div className="flex items-start justify-between">
                            <div className="flex-1">
                                <div className="flex items-center gap-2">
                                    <Building2 className="w-5 h-5 text-muted-foreground" />
                                    <CardTitle className="text-xl">{name || "Company Name"}</CardTitle>
                                </div>
                                <div className="flex items-center gap-2 mt-1">
                                    <Briefcase className="w-4 h-4 text-muted-foreground" />
                                    <CardDescription>
                                        {industry || "Industry not specified"}
                                    </CardDescription>
                                </div>
                            </div>
                            {icpFit !== undefined && (
                                <CardAction>
                                    <div className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border text-muted-foreground">
                                        <Target className="w-3.5 h-3.5" />
                                        {icpFit}% ICP Fit
                                    </div>
                                </CardAction>
                            )}
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="flex flex-col gap-4">
                            {domain && (
                                <div className="grid gap-1">
                                    <div className="flex items-center gap-2">
                                        <Globe className="w-4 h-4 text-muted-foreground" />
                                        <p className="text-xs font-medium text-muted-foreground">Domain</p>
                                    </div>
                                    <p className="text-sm ml-6">{domain}</p>
                                </div>
                            )}

                            {website && (
                                <div className="grid gap-1">
                                    <div className="flex items-center gap-2">
                                        <Globe className="w-4 h-4 text-muted-foreground" />
                                        <p className="text-xs font-medium text-muted-foreground">Website</p>
                                    </div>
                                    <a
                                        href={website.startsWith('http') ? website : `https://${website}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-sm text-blue-600 dark:text-blue-400 hover:underline ml-6 flex items-center gap-1"
                                    >
                                        {website}
                                        <ExternalLink className="w-3 h-3" />
                                    </a>
                                </div>
                            )}

                            {location && (
                                <div className="grid gap-1">
                                    <div className="flex items-center gap-2">
                                        <MapPin className="w-4 h-4 text-muted-foreground" />
                                        <p className="text-xs font-medium text-muted-foreground">Location</p>
                                    </div>
                                    <p className="text-sm ml-6">{location}</p>
                                </div>
                            )}

                            {(employeeCount || revenue) && (
                                <div className="grid grid-cols-2 gap-4">
                                    {employeeCount && (
                                        <div className="grid gap-1">
                                            <div className="flex items-center gap-2">
                                                <Users className="w-4 h-4 text-muted-foreground" />
                                                <p className="text-xs font-medium text-muted-foreground">Employees</p>
                                            </div>
                                            <p className="text-sm ml-6">{employeeCount}</p>
                                        </div>
                                    )}
                                    {revenue && (
                                        <div className="grid gap-1">
                                            <div className="flex items-center gap-2">
                                                <DollarSign className="w-4 h-4 text-muted-foreground" />
                                                <p className="text-xs font-medium text-muted-foreground">Revenue</p>
                                            </div>
                                            <p className="text-sm ml-6">{revenue}</p>
                                        </div>
                                    )}
                                </div>
                            )}

                            {description && (
                                <div className="grid gap-1">
                                    <div className="flex items-center gap-2">
                                        <FileText className="w-4 h-4 text-muted-foreground" />
                                        <p className="text-xs font-medium text-muted-foreground">Description</p>
                                    </div>
                                    <p className="text-sm text-muted-foreground line-clamp-3 ml-6">{description}</p>
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>
        )
    }

    if (role === 'event') {
        // Parse event data from content
        let eventData;
        if (!content) {
            eventData = DEFAULT_EVENT_DATA;
        } else if (typeof content === 'string') {
            try {
                eventData = JSON.parse(content);
            } catch (e) {
                eventData = DEFAULT_EVENT_DATA;
            }
        } else {
            eventData = content;
        }

        const { title, description, timestamp, location } = eventData;

        return (
            <div className="flex justify-center w-full my-6">
                <Card className="w-full max-w-md p-0">
                    <CardContent className="p-4">
                        <div className="flex items-start gap-3">
                            <div className="flex-shrink-0 mt-0.5 text-muted-foreground">
                                <Info className="size-5" />
                            </div>
                            <div className="flex-1 min-w-0">
                                <CardTitle className="text-base mb-1">
                                    {title}
                                </CardTitle>
                                {description && (
                                    <CardDescription className="mt-1">
                                        {description}
                                    </CardDescription>
                                )}
                                {(timestamp || location) && (
                                    <div className="flex flex-wrap items-center gap-3 mt-2 text-xs text-muted-foreground">
                                        {timestamp && (
                                            <div className="flex items-center gap-1">
                                                <Clock className="size-3" />
                                                <span>{timestamp}</span>
                                            </div>
                                        )}
                                        {location && (
                                            <div className="flex items-center gap-1">
                                                <MapPin className="size-3" />
                                                <span>{location}</span>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    // Agent message with markdown
    return (
        <div className="flex justify-start">
            <Card
                className="p-3 max-w-full border-none shadow-none bg-white">
                <CardContent
                    className="p-0">
                    <article className="markdown-body break-words overflow-x-auto max-w-full">
                        <ReactMarkdown>
                            {content}
                        </ReactMarkdown>
                    </article>
                </CardContent>
            </Card >
        </div>
    );
};

export default Message;

