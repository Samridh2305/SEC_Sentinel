import {
    LayoutDashboard,
    Building2,
    FileText,
    GitCompare,
    MessageSquare,
    Settings
} from "lucide-react";


function Sidebar(){
    return(
        <aside className="sidebar">
            <div className="logo">
                SEC SENTINEL
            </div>
            <nav className="sidebar-nav">
                <div className="nav-item active">
                    <LayoutDashboard size={18} />
                    <span>Dashboard</span>
                </div>

                <div className="nav-item">
                    <Building2 size={18} />
                    <span>Companies</span>
                </div>

                <div className="nav-item">
                    <FileText size={18} />
                    <span>Filings</span>
                </div>

                <div className="nav-item">
                    <GitCompare size={18} />
                    <span>Comparisons</span>
                </div>

                <div className="nav-item">
                    <MessageSquare size={18} />
                    <span>Ask Sentinel</span>
                </div>
            </nav>
            <div className="sidebar-bottom">
                <div className="nav-item">
                    <Settings size={18} />
                    <span>Settings</span>
                </div>
            </div>
        </aside>
    );
}
export default Sidebar;